import azure.functions as func
import logging
import os
from pydantic import BaseModel, Field
from pydantic import ValidationError
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
from functions import pdf_processor
from functions import connections
import datetime as dt
from datetime import datetime

DOTENV_FILEPATH = os.path.join('.env')
DEV_ENV = os.path.exists(DOTENV_FILEPATH)
print("DEV ENV: ", DEV_ENV)
if DEV_ENV:
    print("LOADING ENV VARIABLES...")
    load_dotenv(DOTENV_FILEPATH, override=True)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CHUNK_SIZE  = os.getenv("ZZ_FILE_PROCESSING_DEFAULT_CHUNK_SIZE")

AZURE_STORAGE_CONNECTION_STRING = os.getenv("ZZ_AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("ZZ_AZURE_STORAGE_CONTAINER")
AZURE_STORAGE_CONTAINER_FOLDER = os.getenv("ZZ_AZURE_STORAGE_CONTAINER_FOLDER") or ""
AZURE_FUNCTION_TRIGGER_PATH = AZURE_STORAGE_CONTAINER + AZURE_STORAGE_CONTAINER_FOLDER + "/{name}"

class doc_details(BaseModel):
    company_name: str = Field(None)
    industry_name: str = Field(None)
    publication_date: str = Field(None)

class OutputDocument(BaseModel):
    content_id: str
    doc_name: str
    content_doc_pages: List[int]
    content_tokens: int
    doc_words: int
    doc_url: str
    doc_path: str
    content: str
    doc_details: Optional[doc_details]
    doc_id: str
    content_embedding: List[float]
    doc_tags: Optional[List[str]]
    processed_datetime: datetime

app = func.FunctionApp()

@app.function_name(name="UploadedFileProcessing")
@app.blob_trigger(arg_name="uploadedfile", path=AZURE_FUNCTION_TRIGGER_PATH, connection="ZZ_AZURE_STORAGE_CONNECTION_STRING") 
def doc_processing(uploadedfile: func.InputStream):
    try:
        logging.info(f"##### Processing new file: {uploadedfile.name} #####")
        
        folder_path, file_name = os.path.split(uploadedfile.name)
        file = uploadedfile.read()
        blob_url = uploadedfile.uri
        
        logger.info('##### Reading & extracting content from file #####')
        data_df = pdf_processor.pdf_to_df(connections.AZURE_DI_MODEL_ID, connections.DOC_INTEL_CLIENT, file, file_name, blob_url, folder_path)
        
        logger.info('##### Chunking file contents #####')
        data_df_chunk = pdf_processor.create_chunks(connections.DOC_INTEL_CLIENT, data_df, CHUNK_SIZE, file_name)
        
        logger.info('##### Creating text embeddings for file content chunks #####')
        data_df_embedding  = pdf_processor.document_embedding(connections.EMBEDDING_MODEL, data_df_chunk)
        
        output_df = data_df_embedding.rename(columns={'chunk_content': 'content','chunk_doc_pages':'content_doc_pages', 
                                                    'chunk_token_len':'content_tokens','doc_word_length':'doc_words',
                                                    'chunk_embedding':'content_embedding','chunk_id':'content_id','tags':'doc_tags'}).drop(columns = 'chunk_titles')

        output_df['processed_datetime'] = dt.datetime.utcnow() 
        logger.info('##### Uploading the documents to Azure AI Search Index #####')
        documents = output_df.to_dict(orient='records')
        try:
            validated_documents = [OutputDocument(**doc) for doc in documents]
        except ValidationError as e:
            logger.error(f'Document validation failed: {e}')
            raise
        else:
            result = connections.AI_SEARCH_CLIENT.upload_documents(documents=[doc.model_dump() for doc in validated_documents])
            logger.info('###### Upload of new document succeeded: {}'.format(result[0].succeeded))
    
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        raise