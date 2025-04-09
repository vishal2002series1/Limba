import openai
import logging
import yaml
from yaml.loader import SafeLoader
import os
import json

logger = logging.getLogger(__name__)
logger.info("Check")

openai.api_type = 'azure'
openai.api_version =  os.getenv("ZZ_OPENAI_API_VERSION")
openai.api_base = os.getenv("ZZ_OPENAI_API_BASE")
openai.api_key = os.getenv("ZZ_OPENAI_API_KEY")

OPENAI_GTP4_32K_DEPLOYMENT = os.getenv("ZZ_OPENAI_GTP4_32K_DEPLOYMENT")

def summary_prompt_creation(final_content,word_limit,response_dict):
    summary_response= None
    try:
        messages =  [{"role":"system","content":f"""As an AI assistant, your task is to generate a detailed summary of the content of the input document.The document may contain tables, which are enclosed within <table-start> and </table-end> tags.Your summary should capture the main points from the document, including the information presented in the tables.The summary should be detailed and should not exceed {word_limit} words"""}]
        print("messages..................",messages)
        messages.append({"role": "user", "content": final_content})

        summary_response = openai.ChatCompletion.create(
            engine=OPENAI_GTP4_32K_DEPLOYMENT,
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

        article_response = openai.ChatCompletion.create(
            engine=OPENAI_GTP4_32K_DEPLOYMENT,
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

    summary_response = openai.ChatCompletion.create(
        engine=OPENAI_GTP4_32K_DEPLOYMENT,
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

        summary_response = openai.ChatCompletion.create(
            engine=OPENAI_GTP4_32K_DEPLOYMENT,
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

document_classifier_template = """You are a financial services professional. Given a question (“QUESTION”), identify the type of document (“DOCUMENT TYPE”) required to answer the question from one of the categories provided below. Each category is provided with the Document Type and Document Description. Your job is to identify the type of document (“DOCUMENT TYPE”) based on the information asked in the question.
Category 1:
Document Type: Earnings call transcripts
Document Description: A company's earnings call transcript contains a comprehensive overview of its financial performance, strategic initiatives, industry trends, and future guidance. It includes details about revenue, net income, and other financial metrics, along with analysis of business segments and operational challenges. The transcript often features a Q&A session with analysts and investors. Key topics covered are capital allocation, shareholder returns, risks, and corporate governance. These transcripts are essential for investors and analysts to gain insights into a company's financial health and future prospects.

Category 2:
Document Type: Financial documents
Document Description: Companies' financial documents, such as Form 8-K, Form 10-Q, Form 4, Form 13F, and Form 144, are filed with the U.S. SEC to provide important information to investors and ensure regulatory compliance. Form 8-K reports significant events, Form 10-Q presents quarterly financial updates, Form 4 discloses insider transactions, Form 13F lists institutional investment managers' holdings, and Form 144 notifies the SEC of planned sales of restricted securities. These documents offer transparency into a company's financial condition, management changes, insider activity, and investment positions.

Category 3:
Document Type: News articles
Document Description: Company news articles contain information about a company's financial performance, business developments, product launches, leadership changes, legal matters, industry analysis, CSR initiatives, and stock market performance. They provide insights into a company's operations, strategy, and market standing. Readers should verify information from reliable sources and official filings for accuracy and objectivity. These articles are useful for investors, analysts, and stakeholders to stay informed about a company's activities and financial health.

Category 4:
Document Type: Unsure
Document Description: Any documents which do not fall under the above 3 categories would fall under this category

Please format your answer as follows:
DOCUMENT TYPE: <Type of Document based on the 4 categories provided>

Example is as below:

You are a financial services professional. Given a question (“QUESTION”), identify the type of document (“DOCUMENT TYPE”) required to answer the question from one of the categories provided below. Each category is provided with the Document Type and Document Description. Your job is to identify the type of document (“DOCUMENT TYPE”) based on the information asked in the question.
Category 1:
Document Type: Earnings call transcripts
Document Description: A company's earnings call transcript contains a comprehensive overview of its financial performance, strategic initiatives, industry trends, and future guidance. It includes details about revenue, net income, and other financial metrics, along with analysis of business segments and operational challenges. The transcript often features a Q&A session with analysts and investors. Key topics covered are capital allocation, shareholder returns, risks, and corporate governance. These transcripts are essential for investors and analysts to gain insights into a company's financial health and future prospects.

Category 2:
Document Type: Financial documents
Document Description: Companies' financial documents, such as Form 8-K, Form 10-Q, Form 4, Form 13F, and Form 144, are filed with the U.S. SEC to provide important information to investors and ensure regulatory compliance. Form 8-K reports significant events, Form 10-Q presents quarterly financial updates, Form 4 discloses insider transactions, Form 13F lists institutional investment managers' holdings, and Form 144 notifies the SEC of planned sales of restricted securities. These documents offer transparency into a company's financial condition, management changes, insider activity, and investment positions.

Category 3:
Document Type: News articles
Document Description: Company news articles contain information about a company's financial performance, business developments, product launches, leadership changes, legal matters, industry analysis, CSR initiatives, and stock market performance. They provide insights into a company's operations, strategy, and market standing. Readers should verify information from reliable sources and official filings for accuracy and objectivity. These articles are useful for investors, analysts, and stakeholders to stay informed about a company's activities and financial health.

Category 4:
Document Type: Unsure
Document Description: Any documents which do not fall under the above 3 categories would fall under this category

Please format your answer as follows:
DOCUMENT TYPE: <Type of Document based on the 4 categories provided>

QUESTION: What are the key takeaways from Delta Airline's earnings call?
DOCUMENT TYPE: Earnings call transcripts


You are a financial services professional. Given a question (“QUESTION”), identify the type of document (“DOCUMENT TYPE”) required to answer the question from one of the categories provided below. Each category is provided with the Document Type and Document Description. Your job is to identify the type of document (“DOCUMENT TYPE”) based on the information asked in the question.
Category 1:
Document Type: Earnings call transcripts
Document Description: A company's earnings call transcript contains a comprehensive overview of its financial performance, strategic initiatives, industry trends, and future guidance. It includes details about revenue, net income, and other financial metrics, along with analysis of business segments and operational challenges. The transcript often features a Q&A session with analysts and investors. Key topics covered are capital allocation, shareholder returns, risks, and corporate governance. These transcripts are essential for investors and analysts to gain insights into a company's financial health and future prospects.

Category 2:
Document Type: Financial documents
Document Description: Companies' financial documents, such as Form 8-K, Form 10-Q, Form 4, Form 13F, and Form 144, are filed with the U.S. SEC to provide important information to investors and ensure regulatory compliance. Form 8-K reports significant events, Form 10-Q presents quarterly financial updates, Form 4 discloses insider transactions, Form 13F lists institutional investment managers' holdings, and Form 144 notifies the SEC of planned sales of restricted securities. These documents offer transparency into a company's financial condition, management changes, insider activity, and investment positions.

Category 3:
Document Type: News articles
Document Description: Company news articles contain information about a company's financial performance, business developments, product launches, leadership changes, legal matters, industry analysis, CSR initiatives, and stock market performance. They provide insights into a company's operations, strategy, and market standing. Readers should verify information from reliable sources and official filings for accuracy and objectivity. These articles are useful for investors, analysts, and stakeholders to stay informed about a company's activities and financial health.

Category 4:
Document Type: Unsure
Document Description: Any documents which do not fall under the above 3 categories would fall under this category

Please format your answer as follows:
DOCUMENT TYPE: <Type of Document based on the 4 categories provided>

QUESTION: What is the news saying about Marriot's latest annual report?
DOCUMENT TYPE: News articles


You are a financial services professional. Given a question (“QUESTION”), identify the type of document (“DOCUMENT TYPE”) required to answer the question from one of the categories provided below. Each category is provided with the Document Type and Document Description. Your job is to identify the type of document (“DOCUMENT TYPE”) based on the information asked in the question.
Category 1:
Document Type: Earnings call transcripts
Document Description: A company's earnings call transcript contains a comprehensive overview of its financial performance, strategic initiatives, industry trends, and future guidance. It includes details about revenue, net income, and other financial metrics, along with analysis of business segments and operational challenges. The transcript often features a Q&A session with analysts and investors. Key topics covered are capital allocation, shareholder returns, risks, and corporate governance. These transcripts are essential for investors and analysts to gain insights into a company's financial health and future prospects.

Category 2:
Document Type: Financial documents
Document Description: Companies' financial documents, such as Form 8-K, Form 10-Q, Form 4, Form 13F, and Form 144, are filed with the U.S. SEC to provide important information to investors and ensure regulatory compliance. Form 8-K reports significant events, Form 10-Q presents quarterly financial updates, Form 4 discloses insider transactions, Form 13F lists institutional investment managers' holdings, and Form 144 notifies the SEC of planned sales of restricted securities. These documents offer transparency into a company's financial condition, management changes, insider activity, and investment positions.

Category 3:
Document Type: News articles
Document Description: Company news articles contain information about a company's financial performance, business developments, product launches, leadership changes, legal matters, industry analysis, CSR initiatives, and stock market performance. They provide insights into a company's operations, strategy, and market standing. Readers should verify information from reliable sources and official filings for accuracy and objectivity. These articles are useful for investors, analysts, and stakeholders to stay informed about a company's activities and financial health.

Category 4:
Document Type: Unsure
Document Description: Any documents which do not fall under the above 3 categories would fall under this category

Please format your answer as follows:
DOCUMENT TYPE: <Type of Document based on the 4 categories provided>

QUESTION: What are the key takeaways from American Airline’s 2023 8-K report?
DOCUMENT TYPE: Financial documents
"""

question_classifier_template = """You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Negative Case Questions include questions about Personal Identifiable Information, investment recommendations, legal, risk and compliance, market activity, tax structuring, tax liabilities, tax reporting and personal financial information, such as net worth and compensation.

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

Examples are provided below:
Example 1:

You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

QUESTION: What are the key takeaways from Hilton's quarter 1 2023 earnings call?
Question Type: Base Case Question

Example 2:

You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

QUESTION: Compare the Q1 2023 earnings call results from American Airlines, Delta Airlines and JetBlue Airlines.
Question Type: Comparative Question

Example 3:

You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

QUESTION: Have any of my clients not added beneficiaries?
Question Type: Client Data related Question

Example 4:

You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

QUESTION: What is the social security number of client John Smith?
Question Type: Negative Case Question

Example 5:

You are a financial services professional. Given a question (“QUESTION”), identify the type of question ("Question Type") from one of the options provided below based on the information asked in the question. If none of the options are applicable, then please return "Unsure" as output.
Option 1: Base Case Question
Option 2: Comparative Question
Option 3: Client Data related Question
Option 4: Negative Case Question

Please format your answer as follows:
Question Type: <Type of Question based on the 4 options provided>

QUESTION: What was the compensation of Jane Doe last quarter?
Question Type: Negative Case Question
"""

question_splitting_template = """You are a financial services professional. Given a comparative question (“QUESTION”), identify all companies/timelines which are asked to compare in the question.
Once you have identified the companies/timelines, split the question and come up with a separate question for each company/timeline based on the examples provided below.

Please format your answer as follows:
QUESTION: <Question that was asked initially to compare>
ANSWER: <Questions after splitting>

Example 1:

You are a financial services professional. Given a comparative question (“QUESTION”), identify all companies/timelines which are asked to compare in the question.
Once you have identified the companies/timelines, split the question and come up with a separate question for each company/timeline based on the examples provided below.

Please format your answer as follows:
QUESTION: <Question that was asked initially to compare>
ANSWER: <Questions after splitting>

QUESTION: Compare the Q1 2023 earnings call results from American Airlines, Delta Airlines and JetBlue Airlines.
ANSWER:
1. What are the financial results of American Airlines in Q1 2023?
2. What are the financial results of Delta Airlines in Q1 2023?
3. What are the financial results of JetBlue Airlines in Q1 2023?

Example 2:

You are a financial services professional. Given a comparative question (“QUESTION”), identify all companies/timelines which are asked to compare in the question.
Once you have identified the companies/timelines, split the question and come up with a separate question for each company/timeline based on the examples provided below.

Please format your answer as follows:
QUESTION: <Question that was asked initially to compare>
ANSWER: <Questions after splitting>

QUESTION: Compare the financial results from American Airlines' Earnings Report Transcript from the first quarter of 2023 with financial results from the last quarter of 2022
ANSWER:
1. What are the financial results from American Airlines' Earnings Report Transcript from the first quarter of 2023?
2. What are the financial results from American Airlines' Earnings Report Transcript from the last quarter of 2022?

Example 3:

You are a financial services professional. Given a comparative question (“QUESTION”), identify all companies/timelines which are asked to compare in the question.
Once you have identified the companies/timelines, split the question and come up with a separate question for each company/timeline based on the examples provided below.

Please format your answer as follows:
QUESTION: <Question that was asked initially to compare>
ANSWER: <Questions after splitting>

QUESTION: Provide and compare recent analysts’ price targets for American Airlines and Southwest Airlines.
ANSWER:
1. What is the recent analysts' price target for American Airlines?
2. What is the recent analysts' price target for Southwest Airlines?

"""

negative_case_template = """You are a financial services professional. Given a question (“QUESTION”), identify the category of question ("QUESTION CATEGORY") from one of the options provided below and generate a response (“RESPONSE”) based on the information asked in the question. If none of the options are applicable, then please return “Unsure” as output.

QUESTION CATEGORY Options:
Option 1: Personal Identifiable Information (PII)
Option 2: Personalized Investment Recommendation
Option 3: Permissions
Option 4: Legal, Risk and Compliance
Option 5: Market Activity
Option 6: Other

If the QUESTION CATEGORY is Personal Identifiable Information (PII) return the following:
“I’m sorry but I cannot provide or access any personal identifiable information, such as social security numbers, home addresses, credit card information, passport information, and medical records.”

If the QUESTION CATEGORY is Personalized Investment Recommendation return the following:
“I’m sorry but I cannot provide specific investment recommendations tailored to individual profiles or situations. Please consult a financial advisor for more information on individual investment recommendations.”

If the QUESTION CATEGORY is Permissions, return the following:
“I’m sorry but I cannot disclose an individual’s personal financial information, such as compensation and net worth without proper authorization”

If the QUESTION CATEGORY is Legal, Risk and Compliance return the following:
“I’m sorry but I am not qualified to provide advice on legal, risk and compliance questions. For more information, it is recommended to seek advice from professionals who specialize in legal, risk and compliance topics.”

If the QUESTION CATEGORY is Market Activity return the following:
“I’m sorry but I am not able to predict future market activity. Predicting market movements is highly uncertain as they are influenced by a multitude of unpredictable factors.”

If the QUESTION CATEGORY is Other return the following:
“I’m sorry but I do not have the proper authorization or required information to provide an answer for the given question.”

Please format your answer as follows:
QUESTION: <Question that was asked>
QUESTION CATEGORY: <Category which the question contains based on the 6 options above. If none of the options are applicable, then please return "Unsure" as output.>
RESPONSE: <Response based on the question category identified for a particular question>

"""

company_name_template = """
You are a financial services professional. Given a question (“QUESTION”), identify the company from the question ("QUESTION"). If company is not present in ("QUESTION") please return "NA" as output.
"""

def question_completion_model(question,template):
    messages =  [{"role":"system","content":template}]
    messages.append({"role": "assistant", "content": question})

    summary_response = openai.ChatCompletion.create(
        engine=OPENAI_GTP4_32K_DEPLOYMENT,
        messages = messages)

    return summary_response.choices[0].message.content