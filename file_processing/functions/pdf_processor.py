import uuid
import re
import json
import pandas as pd
import datetime
from . import preprocess_functions
from . import llm_extraction
from . import connections

llm = connections.LLM
extract_company_industry = llm_extraction.extract_company_industry
extract_publication_date = llm_extraction.extract_publication_date
Pre_Processing = preprocess_functions.Pre_Processing

import logging

logger = logging.getLogger(__name__)

def assign_tag(blob_uri,config_path):
    value=[]
    with open(config_path, 'r') as f:
        data = json.load(f)
    for i in data.keys():
        x = re.search(i, blob_uri)
        if x:
            value.append(data[i])
    if not value:
        value.append("general")
    return list(set(value))

def pdf_to_df(model_id, DOC_INTEL_CLIENT, file, file_name, blob_url, file_path):
    complete_file_text_list=[]
    text_data_for_publication_date =[]
    complete_file_text= None
    preprocess = Pre_Processing(DOC_INTEL_CLIENT)
    document_source_id = preprocess.datetime_format().split('.')[-1]+'-'+ str(uuid.uuid4())
    final_dataframe_text=pd.DataFrame(columns=['content','doc_name','page_number','token_len','title','doc_word_length', 'doc_url','doc_path', 'doc_details','doc_id','tags'])
    try:
        extracted_text = preprocess.extract_text_form_recognizer(model_id, file)
        data_updates = preprocess.to_dataframe(extracted_text,file)
        tables =extracted_text.tables
        try:
            for table in tables:
                table_dict = preprocess.extract_table(table)
                if 'page_number' in table_dict.keys():
                    data_updates = preprocess.update_table_info(data_updates,table_dict)

            if len(data_updates)!=0:
                data_updates = preprocess.para_alignment(data_updates)

        except Exception as e :
            logger.exception("Error in pdf_to_df")
            pass

        if 'content' in data_updates.columns:
            data_updates['token_len'] = data_updates['content'].apply(preprocess.get_token_length)
            for text in data_updates['content'].values:
                complete_file_text_list.append(text)

            file_word_length = str(len((" ".join(map(str,complete_file_text_list))).split(" ")))

            data_updates['doc_word_length'] = int(file_word_length)

            for _, row in data_updates.iterrows():
                if int(row['page_number'])<=4:
                    text_data_for_publication_date.append(row['content'])

            complete_file_text =  "\n".join(map(str,text_data_for_publication_date))

            publication_date = extract_publication_date(llm, complete_file_text)

            publication_date = publication_date.replace('-','_').replace(":", "_").replace("/", "_")

            if len(publication_date)>10:
                datetime.datetime.strptime(publication_date,'%d_%b_%Y').strftime('%d_%m_%Y')

            company_industry_details_dict = extract_company_industry(llm, complete_file_text)
            company_name = company_industry_details_dict['company_name']
            industry_name = company_industry_details_dict['industry_name']
            tag = assign_tag(blob_url, './tag_config.json')
            details = {'publication_date':publication_date, "company_name":company_name,"industry_name":industry_name}
            l = data_updates.shape[0]
            data_updates.loc[:,'doc_details'] = [details]*l
            data_updates.loc[:,'tags'] = [tag]*l
            data_updates['doc_name'] = file_name
            data_updates['doc_url'] = blob_url
            data_updates['doc_path'] = file_path
            data_updates['doc_id'] = document_source_id
            data_updates = data_updates[data_updates.token_len>0]
            final_dataframe_text=pd.concat([final_dataframe_text,data_updates],axis=0)
    except Exception as e:
        logger.exception("Error in pdf_to_df")
            
    return final_dataframe_text


def document_embedding(EMBEDDING_MODEL, dataframe):
    try:
        dataframe['chunk_embedding'] = EMBEDDING_MODEL.embed_documents(dataframe['chunk_content'])
        dataframe['chunk_id'] = dataframe.apply(lambda x: str(uuid.uuid4()), axis=1)

    except Exception as e:
        logger.exception("Error in document_embedding")

    return dataframe


def create_chunks(DOC_INTEL_CLIENT, data_df, CHUNK_SIZE, file_name):
    result_df=pd.DataFrame(columns=['chunk_content','doc_name','chunk_doc_pages','chunk_token_len','chunk_titles','doc_word_length','doc_url','doc_path','doc_details','doc_id','tags'])
    try:
        preprocess = Pre_Processing(DOC_INTEL_CLIENT)
        result_df=pd.concat([result_df,preprocess.get_chunks_multiple_pages(data_df,file_name,CHUNK_SIZE)],axis=0)
    except Exception as e:
        logger.exception("Error in create_chunks")
    return result_df