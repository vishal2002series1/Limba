import openai
import logging
import yaml
from yaml.loader import SafeLoader
import os
import json

logger = logging.getLogger(__name__)
logger.info("Check")

with open(r'devConfig.yml') as f:
    configParser = yaml.load(f, Loader=SafeLoader)


dep_gpt4_32k= os.getenv('ZZ_DEPLOYMENT_32K')
#dep_gpt4_32k= configParser['DEPLOYMENT_32K']


def summary_prompt_creation(final_content,word_limit,response_dict):
    summary_response= None
    try:

        messages =  [{"role":"system","content":f"""As an AI assistant, your task is to generate a detailed summary of the content of the input document.The document may contain tables, which are enclosed within <table-start> and </table-end> tags.Your summary should capture the main points from the document, including the information presented in the tables.The summary should be detailed and should not exceed {word_limit} words"""}]
        print("messages..................",messages)
        messages.append({"role": "user", "content": final_content})

        os.environ["OPENAI_API_TYPE"] = configParser["OPENAI_API_TYPE"]
        openai.api_version =  '2023-05-15'
        openai.api_base = os.getenv("ZZ_OPENAI_API_BASE")  #or configParser['OPENAI_API_BASE']
        openai.api_key =os.getenv("ZZ_OPENAI_API_KEY") #or configParser['OPENAI_API_BASE']

        # dep_gpt4_32k= os.getenv('ZZ_DEPLOYMENT_32K')

        summary_response = openai.ChatCompletion.create(
            engine=dep_gpt4_32k,
            messages = messages,
    #         temperature=0,
    #         frequency_penalty=0,
    #         presence_penalty=0,
    #         stop=None
            )
        summary_response = summary_response.choices[0].message.content
    except Exception as e:
        logger.info("Summary prompt creation get failed ")
        response_dict.update({"Error":str(e)})
    return summary_response, response_dict

def article_prompt_creation(final_content,word_limit,response_dict):
    article_response= None
    try:
        messages =  [{"role":"system","content":f"""As an AI assistant, your task is to generate very detailed output content from the provided input document.The input document may contain tables, which are enclosed within <table-start> and </table-end> tags. Your article should capture all points from the document and information presented in the tables.The generated output content length should be always more than {word_limit} words and should be always about 8 paragraphs long. Calculate the length of output total words and if it is below {word_limit} words, then please continue to generate detailed output data until the total length becomes 2000 words. In all cases the output word count should always be more than {word_limit} words."""}]
        print("messages..................",messages)
        messages.append({"role": "user", "content": final_content})

        os.environ["OPENAI_API_TYPE"] = configParser["OPENAI_API_TYPE"]
        openai.api_version =  '2023-05-15'
        openai.api_base = os.getenv("ZZ_OPENAI_API_BASE") #or configParser['OPENAI_API_BASE']
        openai.api_key =os.getenv("ZZ_OPENAI_API_KEY") #or configParser['OPENAI_API_KEY']

        article_response = openai.ChatCompletion.create(
            engine=dep_gpt4_32k,
            messages = messages,
    #         temperature=0,
    #         frequency_penalty=0,
    #         presence_penalty=0,
    #         stop=None
            )
        article_response = article_response.choices[0].message.content
    except Exception as e:
        logger.info("Article prompt creation get failed ")
        response_dict.update({"Error":str(e)})
    return article_response, response_dict



def publication_date_prompt(final_content):
    messages =  [{"role":"system","content":f"You are an AI assistant that helps us to extract date from the document content. Please extract the valid date that is supposed to be the document published data/Signature date coming under the document content mainly in header or in title but it will not be inside the content.\nPlease format the extracted date in MM-DD-YYYY format only. Please return only the date as final output and there should not be any other content which should get generated as part of the final output"}]
    print("messages..................",messages)
    messages.append({"role": "assistant", "content": final_content})
    os.environ["OPENAI_API_TYPE"] = configParser["OPENAI_API_TYPE"]
    openai.api_version =  '2023-05-15'
    openai.api_base = os.getenv("ZZ_OPENAI_API_BASE") #or configParser['OPENAI_API_BASE']

    openai.api_key = os.getenv("ZZ_OPENAI_API_KEY") #or configParser['OPENAI_API_BASE']
    #dep_gpt4_32k= os.getenv('ZZ_DEPLOYMENT_32K')

    summary_response = openai.ChatCompletion.create(
        engine=dep_gpt4_32k,
        messages = messages,
#         temperature=0,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=None
        )

    return summary_response.choices[0].message.content

def company_industry_prompt(final_content):
    company_industry_details = None
    try:
        logger.info("########### inside company and industry generation prompt ################")
        messages =  [{"role":"system","content":f"""As an AI assistant, your task is to tell the company name and industry name from the input document. The industry name is highly corelated to the company name present in the input document.Please show only company name value with  company_name as key tag and industry name value with  industry_name as key tag in the final output. The final output should be in python dictionary format.If the output contains newline characters ('\n') then remove these newline characters from the final output.generate only one key value pair which is most relevant to the input document"""}]
        print("messages..................",messages)
        messages.append({"role": "assistant", "content": final_content})
        os.environ["OPENAI_API_TYPE"] = configParser["OPENAI_API_TYPE"]
        openai.api_version =  '2023-05-15'
        os.environ["OPENAI_API_BASE"] = os.getenv("ZZ_OPENAI_API_BASE")
        openai.api_key = os.getenv("ZZ_OPENAI_API_KEY")

        summary_response = openai.ChatCompletion.create(
            engine=dep_gpt4_32k,
            messages = messages,
    #         temperature=0,
    #         frequency_penalty=0,
    #         presence_penalty=0,
    #         stop=None
            )

        doc_output = summary_response.choices[0].message.content
        company_industry_details = json.loads(doc_output)
        logger.info("########### company and industry generation prompt completed and assigning to dataframe ###############")
    except Exception as e:
        logger.info("############## company and industry details is missing "+str(e))

    return company_industry_details