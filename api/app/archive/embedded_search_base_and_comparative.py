import logging
import datetime
import pandas as pd
import time
import app.archive.news_article_api as news_api

logger = logging.getLogger(__name__)
logger.info("Check")

def embedded_query_question_main(results,query,model_chunk_size,query_id,redis_obj,langchain_openai,question_classifier_prompt_output,research_document_payload,classifier):
    output_text = None

    try:
        logger.info('########## We have found some data from redis db  #######')
        logger.info('########## Starting the lang chain operation ######')

        prompt_input_chunk_list =  [item.get("chunk_id") for sublist in results[1].values() for item in sublist if "chunk_id" in item]
        output_text = langchain_openai({"input_documents": results[0], "question": query}, return_only_outputs=True)
        generated_answer = output_text["output_text"].strip()

        article_and_research_document_payload = {"news_article_widget":news_api.News_Article().get_news(query),"research_document_widget":research_document_payload}

        if generated_answer.__contains__("SOURCES:"):
            logger.info("##### Openai generated a response for the given question")

            chunk_list_utilize_for_summarization = generated_answer.split("SOURCES:")[1].replace(" ","").split(",")

            unused_chunk_list_for_summarization  =[",".join(i for i in prompt_input_chunk_list if i not in chunk_list_utilize_for_summarization)] if prompt_input_chunk_list != chunk_list_utilize_for_summarization else []

            generated_answer_sources = [",".join(generated_answer.split("SOURCES:")[1].strip().replace(" ","").split(",")) if len(generated_answer.split("SOURCES:")[1].strip().split(","))>1 else generated_answer.split("SOURCES:")[1].strip().replace(" ","").split(",")[0]]
            generated_answer_text = generated_answer.split("SOURCES:")[0].strip()

            mapped_chunks = [{'source_name_blob_url':[chunk_key],'chunks_results':chunk_value} for chunk_key,chunk_value in results[3].items()]
            for idx in range(0,len(mapped_chunks)):
                mapped_chunks[idx]['source_name_blob_url'].append(mapped_chunks[idx]['chunks_results'][0]['blob_file_url'])

            mapped_chunks = redis_obj.remove_blob_from_metadata(mapped_chunks,'blob_file_url','chunks_results')
            metrics = {"tokens_used_context_": results[2]}

            payload = {
                'summarized_answer' :generated_answer_text,
                'source' : generated_answer_sources,
                'top_results_chunks' : mapped_chunks,
                'additional_prompt_chunk': unused_chunk_list_for_summarization,
                "req_chunk_size": model_chunk_size,
                "metrics":metrics,
                'query_id': query_id,
                'query_ques': query,
                'query_type': question_classifier_prompt_output,
                'article':article_and_research_document_payload
            }
            return payload
        else:
            logger.info("##### OpenAI not able to find answer")
            mapped_chunks = [{'source_name_blob_url':[chunk_key],'chunks_results':chunk_value} for chunk_key,chunk_value in results[3].items()]
            for idx in range(0,len(mapped_chunks)):
                mapped_chunks[idx]['source_name_blob_url'].append(mapped_chunks[idx]['chunks_results'][0]['blob_file_url'])
            mapped_chunks = redis_obj.remove_blob_from_metadata(mapped_chunks,'blob_file_url','chunks_results')
            metrics = {"tokens_used_context_": results[2]}
            payload = {
                'summarized_answer': generated_answer,
                'source' : [],
                'top_results_chunks': mapped_chunks,
                'additional_prompt_chunk': [",".join(prompt_input_chunk_list)],
                "req_chunk_size": model_chunk_size,
                "metrics": metrics,
                'query_id': query_id,
                'query_ques': query,
                'query_type': question_classifier_prompt_output,
                'article': article_and_research_document_payload
            }
            return payload
    except Exception as e:
        payload = {
                'status':"Error",
                'message': "Error in embedded_query_question_main"}
        return payload

def assign_common_chunk(chunk_list):
    logger.info("############## inside assign common chunk function ############")
    common_chunk_assignment ={}
    for chunk_dict in chunk_list:
        for key,value in chunk_dict.items():
            if key in common_chunk_assignment:
                common_chunk_assignment[key].extend(value)
            else:
                common_chunk_assignment[key] = value
    logger.info("############## assign common chunk function completed ############")
    return common_chunk_assignment

def news_article_widget_payload_creation(data_news_articles,threshold_no_of_days):

    final_news_article =pd.DataFrame(columns=['doc_id', 'blob_file_url', 'publication_date', 'score'])

    today_date = datetime.datetime.now()
    for _, row in data_news_articles.iterrows():
        if row['chunk_source_type'] =="News Articles":
            no_of_days=(today_date-datetime.datetime.strptime(row['publication_date'],'%d_%m_%Y')).days

            if no_of_days<threshold_no_of_days and no_of_days>0:
                if row['doc_id'] not in list(final_news_article['doc_id']):
                    final_news_article.loc[len(final_news_article.index)]=row
                else:
                    duplicate_doc_score=final_news_article[final_news_article['doc_id']==row['doc_id']]['score']
                    if duplicate_doc_score.iloc[0]<row['score']:
                        duplicate_doc_score.loc[duplicate_doc_score.index[0]]=row['score']

    news_article_payload ={"news_article_widget":final_news_article.sort_values(by=['score'], ascending=False).reset_index(drop=True).iloc[:10][['doc_id',"blob_file_url"]].to_dict('records')}
    logger.info("###### news article widget payload send to embedded query endpoint ############")
    return news_article_payload