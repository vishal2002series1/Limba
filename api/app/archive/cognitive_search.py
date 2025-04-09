import re
import requests
import pandas as pd
import json
import logging
import app.archive.blob_fetch_sas_url as sasurl

logger = logging.getLogger(__name__)
logger.info("Check")

class Cognitive_Search():

    def __init__(self):
        pass

    def get_relevant_chunk_indx(self,summarized_answer):
        try:
            relevant_chunks_list = re.findall(r'\[(doc\d\d?\d?)]', summarized_answer)
            length_doc_n = len("doc")

            relevant_chunk_indx = []

            if relevant_chunks_list:
                for chunk in relevant_chunks_list:
                    chunk_number = chunk[length_doc_n: ]
                    if chunk_number!='':
                        relevant_chunk_indx.append(int(chunk_number)-1)
            return relevant_chunk_indx, relevant_chunks_list
        except Exception as e:
            logger.info('Exception in get_relevant_chunk_indx function ', e)

    def get_score(self,citation):
        try:
            score_data=citation['metadata']['chunking']

            score_start_index=score_data.index('Scores=')+7
            score_end_index=score_data[score_start_index:].index(' ')+score_start_index
            score= (100-float(score_data[score_start_index:score_end_index]))/100
            return score
        except Exception as e:
            logger.info('Exception in get_score fucntion', e)

    def clean_summarized_answer(self,summarized_answer):
        try:
            query=r'\[(doc\d\d?\d?)]'
            r = re.compile(query)
            indexes=[[m.start(),m.end()] for m in r.finditer(summarized_answer)]
            diff=0
            for item in indexes:
                item[0]-=diff
                item[1]-=diff
                if summarized_answer[item[0]-1]==' ':
                    summarized_answer=summarized_answer[:item[0]-1]+summarized_answer[item[1]:]
                    diff=diff+item[1]-item[0]+1
                else:
                    summarized_answer=summarized_answer[:item[0]]+summarized_answer[item[1]:]
                    diff=diff+item[1]-item[0]
            return summarized_answer
        except Exception as e:
            logger.info('Exception in get_score fucntion', e)


def create_payload(response_json, query_id, query,container_client,Container,storage_account_name,storage_account_key):
    out= Cognitive_Search()
    summarized_answer=response_json['choices'][0]['messages'][1]['content']
    relevant_chunk_indx, relevant_chunks_list = out.get_relevant_chunk_indx(summarized_answer)
    citations_list=json.loads(response_json['choices'][0]['messages'][0]['content'])['citations']

    i=0
    mapped_chunks=[]
    prompt_input_chunk_list=[]
    for citation in citations_list:
        temp_chunk_dict={}
        result_chunk={'chunks_results':[], 'source_name_blob_url':[]}
        metadata=citation['metadata']['chunking']
        metadata[metadata.index('Scores='):]
        temp_chunk_dict['chunk_id']='doc'+str(i+1)
        temp_chunk_dict['chunk_text']=citation['content']
        temp_chunk_dict['title']=citation['title']
        temp_chunk_dict['score']=out.get_score(citation)
        result_chunk['chunks_results'].append(temp_chunk_dict)
        result_chunk['source_name_blob_url'].append(citation['filepath'])
        blob_sas_url = sasurl.blobUrl.blob_sas_token(container_client,Container,storage_account_name,storage_account_key,citation['filepath'])
        result_chunk['source_name_blob_url'].append(blob_sas_url)
        mapped_chunks.append(result_chunk)
        if i not in relevant_chunk_indx:
            prompt_input_chunk_list.append('doc'+str(i+1))
        i+=1

    payload = {
            'summarized_answer' :out.clean_summarized_answer(summarized_answer),
            'source' : [','.join(list(set(relevant_chunks_list)))] if len(relevant_chunks_list)!=0 else [],
            'top_results_chunks' : mapped_chunks,
            'additional_prompt_chunk': [",".join(prompt_input_chunk_list)],
            'query_id': query_id,
            'query_ques': query
        }
    return payload