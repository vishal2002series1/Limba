from asyncio.log import logger
import redis
from re import L
import json
import pandas as pd
from datetime import date
import datetime
import uuid
from langchain.docstore.document import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField,
    TagField
)
import numpy as np
import time
from app.archive.market_data_api import *

class Redis_DB:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self,host_name,port,embeddings):
        # self.config_dict = config
        self.client=redis.Redis(host=host_name, port=port)
        self.embeddings = embeddings
        self.VECTOR_DIM = 1536
        self.INDEX_NAME = "wam-doc-idx"                 # name of the search index
        self.KEY_FORMAT = "doc:{}:csize:{}:chunk:{}"    # document keys
        self.RESPONSE_KEY_FORMAT = "doc_id:{}:csize:{}:response:{}"
        self.FEEDBACK_KEY_FORMAT = "query_id:{}"
        self.DOCUMENT_SOURCE_ID = "doc_src:{}"
        self.COMPANY_WIDGET_KEY_FORMAT = "doc_company_widget:{}:csize:{}:chunk:{}"
        self.INDUSTRY_WIDGET_KEY_FORMAT = "doc_industry_widget:{}:csize:{}:chunk:{}"
        self.DISTANCE_METRIC = "COSINE"
        self.SCHEMA = [
            TextField("doc_id"),
            TextField("chunk_id"),
            TextField("chunk"),
            TextField("token_len"),
            TextField("file_word_length"),
            TextField("publication_date"),
            TextField("title"),
            TextField("blob_file_url"),
            TagField("document_source_id"),
            TextField("doc_page_number"),
            VectorField("embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": self.VECTOR_DIM, "DISTANCE_METRIC": "COSINE"}),
            TagField("defined_chunk_size"),
            TagField("key_type"),
            TagField("chunk_source_type"),
            TagField("source_type"),
            TextField("company"),
            TextField("industries"),
            TextField("ui_tester_user_name"),
            TextField("chunk_and_feedback_json"),
            TextField("query_question"),
            TextField("datetime"),
            TextField("redis_Response"),
            VectorField("company_widget_embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": self.VECTOR_DIM, "DISTANCE_METRIC": "COSINE"}),
            TagField("data_source_company_widget")
            ]
        self.index_exists = False
        try:
            self.client.ping()
        except Exception as _:
            exception_msg = f"Cant connect to redis for with exception {_}"
            raise Exception(exception_msg)

    def create_index(self):
        try:
            self.client.ft(self.INDEX_NAME).info()
            print("Index already exists")
            self.index_exist = True
            return True
        except:
            # Create RediSearch Index
            if b'OK' == self.client.ft(self.INDEX_NAME).create_index(
                fields = self.SCHEMA
            ):
                self.index_exist = True
            else:
                self.index_exist = False
                print("Index Error")
            return self.index_exist

    def datetime_format(self):

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        return formatted_datetime

    def store_data(self,chunk_data,chunk_size,chunk_size_list):
        #document_source_id = self.datetime_format().split('.')[-1]+'-'+ str(uuid.uuid4())
        result=[]

        logger.info('########### coming in store_data method ########')

        doc_source_dict = self.document_source_db(chunk_data,chunk_size_list)

        for index,chunk in chunk_data.iterrows():
            logger.info('chunk_id of the current chunk is...')
            logger.info(chunk.chunk_id)
            key = self.KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str(chunk.chunk_id))
            logger.info('key created for the current chunk id')
            chunk_source_type = self.get_source_type(chunk.file_url)
            if doc_source_dict is not None:
                pipleline = self.client.pipeline(transaction=False)
                logger.info("######### document source id present in the db ###################")

                chunk_embedding = np.array(chunk.embedding, dtype=np.float32).tobytes()

                chunk_mapping = {"doc_id":chunk.doc_id,"chunk_id":str(chunk.chunk_id),"chunk":chunk.chunk,"doc_page_number":chunk.doc_page_number,"embedding": chunk_embedding,"defined_chunk_size":chunk_size,
                                "token_len":chunk.token_len, "title":chunk.title,"file_word_length":chunk.word_length,"blob_file_url":chunk.file_url,
                                "publication_date":chunk.publication_date,"document_source_id":doc_source_dict['document_source_id'],"chunk_source_type":chunk_source_type}

                logger.info('chunk mapping done with its assocaited metadata')

                pipleline.hset(key, mapping = chunk_mapping)
                res = pipleline.execute()
                result.extend(res)

                if res!=None:
                    logger.info('chunk with its associated metadata inserted into the redis db')
                    keys = self.RESPONSE_KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str("success"))
                    response_mapping = {"document_source_id":doc_source_dict['document_source_id'],"doc_id":chunk.doc_id,"datetime":str(self.datetime_format()),"defined_chunk_size":chunk_size,"redis_Response":"success"}
                    pipleline.hset(keys, mapping = response_mapping)

                pipleline.execute()


            else:
                pipleline = self.client.pipeline(transaction=False)
                logger.info("######## document db start creating #####################")
                chunk_embedding = np.array(chunk.embedding, dtype=np.float32).tobytes()

                chunk_mapping = {"doc_id":chunk.doc_id,"chunk_id":str(chunk.chunk_id),"chunk":chunk.chunk,"doc_page_number":chunk.doc_page_number,"embedding": chunk_embedding,"defined_chunk_size":chunk_size,
                                "token_len":chunk.token_len, "title":chunk.title,"file_word_length":chunk.word_length,"blob_file_url":chunk.file_url,
                                "publication_date":chunk.publication_date,"document_source_id":chunk.document_source_id,"chunk_source_type":chunk_source_type}

                logger.info('chunk mapping done with its assocaited metadata in else part')

                pipleline.hset(key, mapping = chunk_mapping)

                res = pipleline.execute()
                result.extend(res)
                if res!=None:
                    #pipleline = self.client.pipeline(transaction=False)
                    logger.info('chunk with its associated metadata inserted into the redis db')
                    keys = self.RESPONSE_KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str("success"))
                    response_mapping = {"document_source_id":chunk.document_source_id,"doc_id":chunk.doc_id,"datetime":str(self.datetime_format()),"defined_chunk_size":chunk_size,"redis_Response":"success"}
                    pipleline.hset(keys, mapping = response_mapping)

                pipleline.execute()
        logger.info('Returing from store_data method')
        return result


    def response_failure_status(self,doc,chunk_size,error):

        pipleline = self.client.pipeline(transaction=False)
        keys = self.RESPONSE_KEY_FORMAT.format(doc[:200],str(chunk_size),("failure"))
        response_mapping = {"doc_id":str(doc),"datetime":str(self.datetime_format()),"defined_chunk_size":chunk_size,"redis_Response":"failure","error":str(error),"document_source_id":'N/A'}
        pipleline.hset(keys, mapping = response_mapping)

        res = pipleline.execute()
        return res


    def store_data_company_widget(self,chunk_data,chunk_size):
        result=[]

        logger.info('########### coming in store_data method ########')


        for _,chunk in chunk_data.iterrows():
            logger.info('chunk_id of the current chunk is...')
            logger.info(chunk.chunk_id)
            key = self.COMPANY_WIDGET_KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str(chunk.chunk_id))
            logger.info('key created for the current chunk id')

            pipleline = self.client.pipeline(transaction=False)
            logger.info("######## document db start creating #####################")
            chunk_embedding = np.array(chunk.embedding, dtype=np.float32).tobytes()

            chunk_mapping = {"doc_id":chunk.doc_id,"chunk_id":str(chunk.chunk_id),"chunk":chunk.chunk,"doc_page_number":chunk.doc_page_number,"company_widget_embedding": chunk_embedding,"defined_chunk_size":chunk_size,"blob_file_url":chunk.file_url,
                            'data_source_company_widget':chunk.data_source, "company_name":chunk.company_name,'industry_name':chunk.industry_name, 'widget':'True','company_overview':chunk.company_overview,'parent_organization':chunk.parent_organization,
                            'founded_date':chunk.founded_date, 'headquarters':chunk.headquarters,'management_individuals':chunk.management_individuals, 'number_of_employees':chunk.number_of_employees, 'contact_information':chunk.contact_information, 'ticker':chunk.ticker, 'stock_price':chunk.stock_price,
                            'sales':chunk.sales, 'net_income':chunk.net_income, 'earnings_per_share_EPS':chunk.earnings_per_share_EPS, 'net_profit_margin':chunk.net_profit_margin,'website_link':chunk.website_link, 'partnerships':chunk.partnership
                                }

            logger.info('chunk mapping done with its assocaited metadata in else part')

            pipleline.hset(key, mapping = chunk_mapping)

            res = pipleline.execute()
            result.extend(res)
            if res!=None:
                # pipleline = self.client.pipeline(transaction=False)
                logger.info('chunk with its associated metadata inserted into the redis db')
                keys = self.RESPONSE_KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str("success"))
                response_mapping = {"document_source_id":'NA',"doc_id":chunk.doc_id,"datetime":str(self.datetime_format()),"defined_chunk_size":chunk_size,"redis_Response":"success"}
                pipleline.hset(keys, mapping = response_mapping)

            pipleline.execute()
        logger.info('Returning from store_data method')
        return result


    def store_data_feedback(self,chunk_data):
        pipleline = self.client.pipeline(transaction=False)
        for _,chunk in chunk_data.iterrows():
            key = self.FEEDBACK_KEY_FORMAT.format(str(chunk.chunk_and_feedback_json['query_id']))
            chunk_mapping = {"query_question":chunk.query_question,"ui_tester_user_name":str(chunk.ui_tester_user_name),"feedbacks_timestamp":str(chunk.feedbacks_timestamp),
                "chunk_and_feedback_json":json.dumps(chunk.chunk_and_feedback_json),'key_type':"feedbacks"}
            #feedback_json = json.dumps(chunk_mapping['chunk_and_feedback_json'])

            pipleline.hset(key,mapping =chunk_mapping)

        res = pipleline.execute()
        return res


    def get_recency_search_score(self,results,no_of_chunks,recency_factor):
        logger.info('Recency function started')
        data_chunks=pd.DataFrame(columns=['id','payload','vector_score','doc_id','chunk_id','chunk','doc_page_number','defined_chunk_size','token_len','title','file_word_length','blob_file_url','publication_date','score'])
        for result in results.docs:
            data_chunks.loc[len(data_chunks.index)]=[result.id,result.payload,result.vector_score,result.doc_id,result.chunk_id,result.chunk,result.doc_page_number,result.defined_chunk_size,result.token_len,result.title,result.file_word_length,result.blob_file_url,result.publication_date,1-float(result.vector_score)]

        recency_score_list=[]
        recency_search_score_list=[]
        #recency_factor=0.1
        query_run_date=date.today().strftime('%d-%m-%Y')
        last_date_in_system='28-04-2020'
        days_difference=(datetime.datetime.strptime(query_run_date,'%d-%m-%Y')-datetime.datetime.strptime(last_date_in_system,'%d-%m-%Y')).days
        for i, row in data_chunks.iterrows():
            try:
                if row["publication_date"]!='':
                    logger.info('Fetched publication date, implementing the date format')
                    if len(row["publication_date"])<=10:
                        days_diff_with_pub_date=(datetime.datetime.strptime(query_run_date,'%d-%m-%Y')-datetime.datetime.strptime(row['publication_date'].replace('_','-'),'%d-%m-%Y')).days
                    elif len(row["publication_date"])>10:
                        if '_' in row["publication_date"]:
                            days_diff_with_pub_date=(datetime.datetime.strptime(query_run_date,'%d-%m-%Y')-datetime.datetime.strptime((datetime.datetime.strptime(row['publication_date'],'%d_%b_%Y').strftime('%d-%m-%Y')),'%d-%m-%Y')).days
                        elif '-' in row["publication_date"]:
                            days_diff_with_pub_date=(datetime.datetime.strptime(query_run_date,'%d-%m-%Y')-datetime.datetime.strptime((datetime.datetime.strptime(row['publication_date'],'%d-%b-%Y').strftime('%d-%m-%Y')),'%d-%m-%Y')).days
                        else:
                            recency_score=0
                            recency_search_score=0
                    recency_score=(days_difference-days_diff_with_pub_date)/days_difference
                    recency_search_score=row['score']*(1-recency_factor)+recency_score*recency_factor
                elif row["publication_date"]=='':
                    logger.info('Publication date empty')
                    recency_score=0
                    recency_search_score=0

            except Exception as e:
                print('Exception in Recency Search Score', e)
                logger.info('Exception in Recency Search Score, found another publication date format apart from three mentioned date format')
                recency_score=0
                recency_search_score=0
                pass
            recency_score_list.append(recency_score)
            recency_search_score_list.append(recency_search_score)
        data_chunks['recency_score']=recency_score_list
        data_chunks['recency_search_score']=recency_search_score_list
        logger.info('Recency search completed')
        return data_chunks.sort_values(by=['recency_search_score'], ascending=False).reset_index(drop=True).iloc[:no_of_chunks]

    def search_redis(self,embeddings,recency_factor,user_query,chunk_numbers= 15,score_threshold=0,chunk_size=300):
        index_name=self.INDEX_NAME
        MODEL_TOKEN_CONFIG = {"gpt4": 8192, "open-ai-am": 4096}
        # model_max_token_limit = MODEL_TOKEN_CONFIG.get(self.config_dict['OPENAI_GPT4_DEPLOYMENT'],None)
        model_max_token_limit = 8192
        prompt_token = 1500
        search_total_tokens = model_max_token_limit - prompt_token

        embedded_query = embeddings.embed_query(user_query)

        base_query = f"(@defined_chunk_size:{{{chunk_size}}} -@chunk_source_type:{{Research Document}})=>[KNN {chunk_numbers} @embedding $vector AS vector_score]"
        query = (
            Query(base_query)
            .return_fields("doc_id","chunk_id","chunk","doc_page_number","vector_score","defined_chunk_size",
                           "token_len","title","file_word_length","blob_file_url","publication_date")
            .sort_by("vector_score")
            .paging(0, chunk_numbers)
          #  .dialect(2)
        )
        params_dict = {"vector": np.array(embedded_query).astype(dtype=np.float32).tobytes()}

        # perform vector search
        results = self.client.ft(index_name).search(query, params_dict)
        #news_article_widget_dataframe,news_article_start_time = self.news_article_widget(chunk_size,index_name,params_dict)
        research_document_widget_payload = self.research_document_widget(chunk_size,index_name,params_dict)
        company_widget_payload = self.company_level_widget(chunk_size,index_name,params_dict)

        df=self.get_recency_search_score(results,5,recency_factor)

        docs_and_scores = []
        docs_and_chunks = {}
        raw_doc_and_chunks ={}
        token_len_count = 0

        # for result in results.docs:
        for i, result in df.iterrows():

            logger.info('Started looping the results in redis search')
            token_len_count = token_len_count + int(result.token_len)
            if token_len_count > search_total_tokens:
                token_len_count = token_len_count - int(result.token_len)

                break
            docs_and_scores.append((
                Document(
                    page_content=result.chunk, metadata={"source":result.doc_id,"chunk_id":str(result.chunk_id),"doc_page_number":result.doc_page_number,"defined_chunk_size":result.defined_chunk_size,"chunk_token_len":result.token_len,"score":1-float(result.vector_score),
                                                         'title': result.title,"file_word_length":result.file_word_length,"blob_file_url": result.blob_file_url,
                                                         "publication_date":result.publication_date,"recency_search_score":result.recency_search_score,"recency_factor":recency_factor}
                ),
                float(result.vector_score),
            ))

            getdoc_name = docs_and_chunks.get(result.doc_id,None)
            if getdoc_name and 1-float(result.vector_score) >= score_threshold:
                docs_and_chunks[result.doc_id].append({'chunk_text':result.chunk,"chunk_id":str(result.chunk_id),"doc_page_number":result.doc_page_number,"defined_chunk_size":result.defined_chunk_size,"chunk_token_len":result.token_len,"score":1-float(result.vector_score),
                                                       'title': result.title,"file_word_length":result.file_word_length,"publication_date":result.publication_date,
                                                       "blob_file_url": result.blob_file_url,"recency_search_score":result.recency_search_score,"recency_factor":recency_factor})

            else:
                docs_and_chunks[result.doc_id] = [{'chunk_text':result.chunk,"chunk_id":str(result.chunk_id),"doc_page_number":result.doc_page_number,"defined_chunk_size":result.defined_chunk_size,"chunk_token_len":result.token_len,"score":1-float(result.vector_score),
                                                   'title': result.title,"file_word_length":result.file_word_length,"publication_date":result.publication_date,
                                                   "blob_file_url": result.blob_file_url,"recency_search_score":result.recency_search_score,"recency_factor":recency_factor}]


        # for result in results.docs:
        for i, result in df.iterrows():

            getdoc_name = raw_doc_and_chunks.get(result.doc_id,None)
            if getdoc_name and 1-float(result.vector_score) >= score_threshold:
                raw_doc_and_chunks[result.doc_id].append({'chunk_text':result.chunk,"chunk_id":str(result.chunk_id),"doc_page_number":result.doc_page_number,"defined_chunk_size":result.defined_chunk_size,"chunk_token_len":result.token_len,"score":1-float(result.vector_score),
                                                          'title': result.title,"file_word_length":result.file_word_length,"publication_date":result.publication_date,
                                                          "blob_file_url": result.blob_file_url,"recency_search_score":result.recency_search_score,"recency_factor":recency_factor})
            else:
                raw_doc_and_chunks[result.doc_id] = [{'chunk_text':result.chunk,"chunk_id":str(result.chunk_id),"doc_page_number":result.doc_page_number,"defined_chunk_size":result.defined_chunk_size,"chunk_token_len":result.token_len,"score":1-float(result.vector_score),
                                                      'title': result.title,"file_word_length":result.file_word_length,"publication_date":result.publication_date,
                                                      "blob_file_url": result.blob_file_url,"recency_search_score":result.recency_search_score,"recency_factor":recency_factor}]

        logger.info('Redis search completed')

        return [doc for doc, score in docs_and_scores if 1 - score > score_threshold],docs_and_chunks,token_len_count,raw_doc_and_chunks,research_document_widget_payload,company_widget_payload
        #return results


    def remove_blob_from_metadata(self,data,url,chunk_results):
        mapped_chunks = [
        {
            outer_key: [
            {inner_key: inner_value for inner_key, inner_value in inner_dict.items() if inner_key != url}
            for inner_dict in outer_value]if outer_key == chunk_results else outer_value for outer_key, outer_value in dictionary.items()}for dictionary in data]

        return mapped_chunks


    def get_source_type(self,file_url):
        logger.info("###### get source type from the blob url #############")
        source_type=''
        query_type = file_url.split('/')[4]
        if "query1" in query_type:
            source_type='Earnings Call Transcripts'
        elif "query2" in query_type:
            source_type='Financial Reports'
        elif "query3" in query_type:
            source_type='News Articles'
        elif "research_document" in query_type:
            source_type = "Research Document"
        else:
            source_type = query_type

        logger.info("###### SOurce type generation completed ###############")
        return source_type


    def document_source_db(self,chunk_data,chunk_size_list):
        pipleline = self.client.pipeline(transaction=False)
        doc_source_dict ={}
        #chunk_size_list = [2000]
        doc_name_field = 'doc_id'
        for _,chunk in chunk_data.iterrows():
            for chunk_size in chunk_size_list:
                resp_keys = self.RESPONSE_KEY_FORMAT.format(chunk.doc_id[:200],str(chunk_size),str("success"))
                if self.client.hexists(resp_keys,doc_name_field):
                    logger.info("################## document exists in redis db, assigning source id from doc_src schema #################")
                    redis_key_pattern = f'doc_src:*'
                    pattern_keys = self.client.keys(redis_key_pattern)
                    for key in pattern_keys:
                        doc_source_key_value =  self.client.hgetall(key)
                        decode_field = {field.decode('utf-8'): value.decode('utf-8') for field, value in doc_source_key_value.items()}
                        for key,file_name in decode_field.items():
                            if file_name[:200]==chunk.doc_id[:200]:
                                doc_source_dict['document_source_id'] =decode_field['document_source_id']

                    return  doc_source_dict
                else:
                    logger.info("###########document source id not exists, creating document db #############")
                    source_type=self.get_source_type(chunk.file_url)
                    key = self.DOCUMENT_SOURCE_ID.format(str(chunk.document_source_id))
                    doc_source_level_mapping = {"document_source_id":chunk.document_source_id,"document_name":chunk.doc_id,"blob_file_url":chunk.file_url,
                                                "publication_date":chunk.publication_date,"company":chunk.company_name,"industries":chunk.industry_name,"source_type":source_type}
                    logger.info("######### document source db moved into execution of chunk mapping ##############")
                    pipleline.hset(key, mapping = doc_source_level_mapping)
                pipleline.execute()
                logger.info("############## new document db assignemnt got completed ####################3")


    def research_document_widget(self,chunk_size,index_name,params_dict):
        data_research_document=pd.DataFrame(columns=['doc_id', 'blob_file_url', 'score','chunk_source_type'])
        base_query =  f"(@defined_chunk_size:{{{chunk_size}}} @chunk_source_type:{{Research Document}})=>[KNN {50} @embedding $vector AS vector_score]"

        query = (
            Query(base_query)
            .sort_by("vector_score")
            .paging(0, 50)
        )

        results =  self.client.ft(index_name).search(query, params_dict)
        logger.info("###### data fetched for research documents from redis ############")
        for doc in results.docs:
            data_research_document.loc[len(data_research_document.index)]=[doc.doc_id,doc.blob_file_url,1-float(doc.vector_score),doc.chunk_source_type]

        df_research_document = data_research_document[['doc_id',"blob_file_url"]].to_dict("records")[0]
        return df_research_document

    def company_level_widget(self,chunk_size,index_name,params_dict):

        company_level_factiva = pd.DataFrame(columns = ["doc_id",'industry','overview','parent_organizations','founded',"headquarters","management"
                                                   ,"employees","contact","ticker","stock_price","sales","net_income",
                                                   "EPS","net_profit_margin","score","website_link","partnerships"])

        company_level_dnb_hoovers = pd.DataFrame(columns=["doc_id","website_link","partnerships","score"])


        base_query_factiva = f"(@defined_chunk_size:{{{chunk_size}}} @data_source_company_widget:{{factiva_company_snapshot}})=>[KNN {1} @company_widget_embedding $vector AS vector_score]"
        base_query_dnb_hoovers = f"(@defined_chunk_size:{{{chunk_size}}} @data_source_company_widget:{{dnb_hoovers_company_report}})=>[KNN {5} @company_widget_embedding $vector AS vector_score]"

        query_factiva = (
            Query(base_query_factiva)
            .sort_by("vector_score")
            .paging(0, 1)
        )

        query_dnb_hoovers = (
            Query(base_query_dnb_hoovers)
            .sort_by("vector_score")
            .paging(0, 5)
        )
        results_factiva =  self.client.ft(index_name).search(query_factiva, params_dict)
        results_dnb_hoovers =  self.client.ft(index_name).search(query_dnb_hoovers, params_dict)

        for doc in results_factiva.docs:
            company_level_factiva.loc[len(company_level_factiva.index)]=[doc.doc_id,doc.industry_name,doc.company_overview,doc.parent_organization,doc.founded_date,
                                                               doc.headquarters,doc.management_individuals,doc.number_of_employees,doc.contact_information,
                                                               doc.ticker,doc.stock_price,doc.sales,doc.net_income,doc.earnings_per_share_EPS,doc.net_profit_margin,
                                                               1-float(doc.vector_score),doc.website_link,doc.partnerships]

        for doc in results_dnb_hoovers.docs:
            company_level_dnb_hoovers.loc[len(company_level_dnb_hoovers.index)]=[doc.doc_id,doc.website_link,doc.partnerships,1-float(doc.vector_score)]

        #company_level_dnb_hoovers_refine = company_level_dnb_hoovers[company_level_dnb_hoovers.doc_id.astype(str).apply(lambda x : company_level_factiva['doc_id'].iloc[0][:-4] in x)]
        company_level_dnb_hoovers_refine = company_level_dnb_hoovers[company_level_dnb_hoovers.doc_id.str.lower().str.replace("_"," ").apply(lambda x : company_level_factiva['doc_id'].iloc[0].replace("_"," ")[:-4].lower() in x)]

        if len(company_level_dnb_hoovers_refine)>0:
            company_level_factiva['website_link'] = company_level_dnb_hoovers_refine['website_link'].iloc[0]
            company_level_factiva['partnerships'] = company_level_dnb_hoovers_refine['partnerships'].iloc[0]

        market_data_dict=fetch_financial_metrics(company_level_factiva.loc[0,'ticker'])

        for market_data_key, value in market_data_dict.items():
            company_level_factiva[market_data_key]=value

        company_level_payload = {"company_overview":company_level_factiva[['industry','overview','parent_organizations',"founded","headquarters","website_link"]].to_dict("records"),
                            "management_overview": company_level_factiva[["management","employees","partnerships","contact"]].to_dict("records"),
                            "market_data":company_level_factiva[['ticker',"stock_price","sales","net_income","EPS","net_profit_margin"]].to_dict("records")}


        return company_level_payload