import uuid
import logging
from langchain.embeddings.openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)
logger.info("Check")

class Document_Embedding():

    def __init__(self,embedding_model_name):
       self.embedding_model_name = embedding_model_name
       self.embeddings = OpenAIEmbeddings(deployment=self.embedding_model_name,chunk_size=1)
       self.response_dict ={}

    def document_embedding(self,dataframe,redis_obj,extract_chunk,filename):
        try:
            dataframe['embeddings'] = self.embeddings.embed_documents(dataframe['content'])
            dataframe['chunk_id'] = dataframe.apply(lambda x: str(uuid.uuid4()), axis=1)
            dataframe = dataframe.rename(columns={'page_number': 'doc_page_number', 'embeddings': 'embedding','content':'chunk','file_name':'doc_id'})
            dataframe['doc_id'] = dataframe['doc_id'].str.replace(' ','_', regex=False)
        except Exception as e:
            logger.info("embedding failed",e)
            for file in filename:
                redis_obj.response_failure_status(file ,str(extract_chunk),error=str(e))
            self.response_dict.update({'Error':str(e)})
        return dataframe, self.response_dict