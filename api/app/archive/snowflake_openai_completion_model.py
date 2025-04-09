import re
import json
import openai
import os
import logging
import yaml
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import os
from yaml.loader import SafeLoader

logger = logging.getLogger(__name__)
logger.info("Check")

openai.api_type = os.environ.get('OPENAI_API_TYPE')
openai.api_version = os.environ.get('OPENAI_API_VERSION')

openai.api_base = os.environ.get('OPENAI_API_BASE')
openai.api_key = os.environ.get('OPENAI_API_KEY')

OPENAI_GTP4_32K_DEPLOYMENT = os.environ.get('OPENAI_GTP4_32K_DEPLOYMENT')

def chat_completion_model(messages):
    return openai.ChatCompletion.create(
        engine=OPENAI_GTP4_32K_DEPLOYMENT,
        messages = messages)


def run_snowflake_query(query,sf_username,sf_password,account,database,schema,warehouse,role,parameters=None):
    response = {}
    try:
        engine = create_engine(URL(
                account = account,
                user = sf_username,
                password = sf_password,
                database = database,
                schema = schema,
                warehouse = warehouse,
                role = role))
        try:
            results = pd.read_sql(query, engine).to_json(orient='records')
        finally:
            engine.dispose()
        response['snowflake_records'] = len(results)
        response['snowflake_results'] = results
        response['snowflake_status'] = "success"

        return response
    except Exception as e:
        print("Error with establishing Snowflake connection...")
        print(e)
        response['snowflake_status'] = "error"
        response['snowflake_error'] = str(e)
        return response


def completion_model_snowflake_sql(sql_query_template,question):

    messages =  [{"role":"system","content":sql_query_template}]
    messages.append({"role": "assistant", "content": question})

    response = chat_completion_model(messages)

    openai_response = response.choices[0].message.content

    status = re.search(r'<status start>\s*(.*?)\s*<status end>', openai_response, re.DOTALL).group(1).strip()
    sql_query = re.search(r'<sql start>\s*(.*?)\s*<sql end>', openai_response, re.DOTALL).group(1).strip()
    logger.info("##### SQL query generated from completion model #######")

    return {"quantative_sql_query":{"sql_query":sql_query,"status":status}}


def completion_model_snowflake_synthesis(query,question,snowflake_data,snowflake_result_template):

    messages =  [{"role":"system","content":snowflake_result_template + str({"sqlQuery":query,"snowflake_results":snowflake_data['snowflake_results']})}]
    messages.append({"role": "assistant", "content": question})

    response = chat_completion_model(messages)

    openai_response = response.choices[0].message.content
    print("openai_response",openai_response)

    status = re.search(r'<status start>\s*(.*?)\s*<status end>', openai_response, re.DOTALL).group(1).strip()
    message = re.search(r'<message start>\s*(.*?)\s*<message end>', openai_response, re.DOTALL).group(1).strip()
    logger.info("##### Synthesis answer generated for structured data #######")

    return {'structured_query_summary': {'message': message,'status':status}}




