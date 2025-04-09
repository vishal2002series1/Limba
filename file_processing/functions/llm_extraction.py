import json
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

def extract_publication_date(LLM, final_content):
    template = """
                You are an AI assistant that helps us to extract date from the document content.
                
                Please extract the valid date that is supposed to be the document published data/Signature date coming under the document content mainly in header or in title but it will not be inside the content.
                
                Please format the extracted date in DD_MM_YYYY format only. 
                
                Please return only the date as final output and there should not be any other content which should get generated as part of the final output. 
                
                If date not found in the input document then please give NA in the final output.
                
                Content: {final_content}
                """
    prompt = PromptTemplate(
                input_variables=["final_content"],
                template=template,
                )
    chain = LLMChain(llm=LLM, prompt=prompt)
    try:
        summary_response = chain.invoke(input=final_content)['text']
        return summary_response
    except Exception as e:
        logger.exception("Error in extract_publication_date")
        raise ValueError(f"Error in extract_publication_date, {e}")

def extract_company_industry(LLM, final_content):
    template = """
                As an AI assistant, your task is to tell the company name and industry name from the input document.
                The industry name is highly corelated to the company name present in the input document.
                
                Please show only company name value with  company_name as key tag and industry name value with  industry_name as key tag in the final output.
                    
                The final output should be in python dictionary format.
                If the output contains newline characters ('\n') then remove these newline characters from the final output.generate only one key value pair which is most relevant to the input document.
                Content: {final_content}
                """
    prompt = PromptTemplate(
                input_variables=["final_content"],
                template=template,
                )
    chain = LLMChain(llm=LLM, prompt=prompt)
    try:
        summary_response = chain.invoke(input=final_content)['text']
        company_industry_details = json.loads(summary_response)
        return company_industry_details
    except json.JSONDecodeError:
        logger.exception("JSON decoding error in extract_company_industry")
        raise ValueError(f"JSON decoding error in extract_company_industry, {e}")
    except Exception as e:
        logger.exception("Error in extract_company_industry")
        raise ValueError(f"Error in extract_publication_date, {e}")
