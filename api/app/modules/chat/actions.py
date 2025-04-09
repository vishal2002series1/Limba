# Imports
import os
from  fastapi import HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime

from . import schema
from .agents import irah_chat_agent, financial_planner_chat_agent
from .endpoint_configurations.wealth_chat_config import wealth_req_config
from .endpoint_configurations.default_config import custom_req_config
from .endpoint_configurations.esg_chat_config import esg_prefix_message, esg_doc_req_config
from .endpoint_configurations.trust_review_chat_config import trust_prefix_message, trust_doc_req_config
from .endpoint_configurations.financial_planner_config import financial_planner_req_config, financial_planner_answer_format
from .endpoint_configurations.unrestricted_chat_config import unrestricted_req_config
from .endpoint_configurations.hoopp_demo_chat_config import hoopp_demo_req_config
from app.irah.connections import AZURE_CONTAINTER_CLIENT
from app.irah.logs import logger
from .agents.advisor_copilot import process_question, process_notes, CombinedQuestionRequest, ProcessNotesRequest



# Main chat agent
def agent_search(llm, req, endpoint_config = custom_req_config):
    """
    Main function used for the chat agent that uses all the default settings.

    Args:
        llm: LLM object used for the main chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and get the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req = schema.ChatRequest(**endpoint_config)).execute_chat()
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Wealth chat agent with filters
def wealth_agent_search(llm, req, endpoint_config = wealth_req_config):
    """
    Function for wealth chat agent endpoint. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the wealth chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and get the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req = schema.ChatRequest(**endpoint_config)).execute_chat()
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# ESG chat agent with filters
def esg_agent_search(llm, req, endpoint_config = esg_doc_req_config, custom_prefix_message = esg_prefix_message):
    """
    Function for ESG chat agent endpoint. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the ESG chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent
        custom_prefix_message: The custom prefix message for the chat agent prompt

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and get the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req=schema.ChatRequest(**endpoint_config)).execute_chat(custom_prefix_message = custom_prefix_message)
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Trust review chat agent with filters
def trust_agent_search(llm, req, endpoint_config = trust_doc_req_config, custom_prefix_message = trust_prefix_message):
    """
    Function for trust chat agent endpoint. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the trust chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent
        custom_prefix_message: The custom prefix message for the chat agent prompt

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and get the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req=schema.ChatRequest(**endpoint_config)).execute_chat(custom_prefix_message = custom_prefix_message)
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Financial Planner chat agent with filters
def financial_planner_agent(llm, req):
    """
    Function for financial planner chat agent endpoint. It uses the financial planner agent as a standalone chat agent (instead of wrapped as a tool).

    Args:
        llm: LLM object used for the wealth chat agent
        req: The request object that contains the question and other details

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")

    # Get the response from the FinancialPlannerChatAgent class and log the end of the chat agent
    response = financial_planner_chat_agent.FinancialPlannerChatAgent(llm, req = req).execute_chat()
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Financial Planner chat agent with filters
def financial_planner_agent_old(llm, req, endpoint_config = financial_planner_req_config, final_answer_format = financial_planner_answer_format):
    """
    Function for wealth chat agent endpoint. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the wealth chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent
        final_answer_format: The final answer format for the chat agent prompt

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and change question in the config to the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req=schema.ChatRequest(**endpoint_config)).execute_chat(final_answer_format = final_answer_format)
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Unrestricted chat agent
def unrestricted_agent_search(llm, req, endpoint_config = unrestricted_req_config):
    """
    Function for unrestricted chat agent endpoint. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the unrestricted chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent
    
    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and change question in the config to the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req=schema.ChatRequest(**endpoint_config)).execute_chat()
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")
    
    return response


# HOOPP demo chat agent with filters
def pe_pension_demo_agent_search(llm, req, endpoint_config = hoopp_demo_req_config):
    """
    Function for Pension demo chat agent endpoint for a healthcare client demo. It uses filters configured in the endpoint configurations.

    Args:
        llm: LLM object used for the HOOPP demo chat agent
        req: The request object that contains the question and other details
        endpoint_config: The configuration for the chat agent

    Returns:
        The response object from the chat agent.
    """
    # Log the start of the chat agent and change question in the config to the question from the request
    logger.info(f"[{datetime.now()}]  actions - calling the IRAHChatAgent class")
    endpoint_config['question'] = req.question

    # Get the response from the IRAHChatAgent class and log the end of the chat agent
    response = irah_chat_agent.IRAHChatAgent(llm, req=schema.ChatRequest(**endpoint_config)).execute_chat()
    logger.info(f"[{datetime.now()}]  actions - response recieved from IRAHChatAgent class")

    return response


# Document retrieval function for endpoint
def get_blob_docs(path, filename):
    """
    Function for the endpoint used to get the actual PDF documents retrieved.
    """
    try:
        logger.info(f"[{datetime.now()}]  actions - file Download initiated")
        container = os.getenv("ZZ_AZURE_STORAGE_CONTAINER")
        doc_path = path.split(f"{container}/")[-1]
        file_path = f"{doc_path}/{filename}"
        blob_client = AZURE_CONTAINTER_CLIENT.get_blob_client(file_path)
        stream = blob_client.download_blob().readall()
        return StreamingResponse(iter([stream]), media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



#####################################################
#
# Advisor Copilot Functions
#
#####################################################

def process_combined_question(req: CombinedQuestionRequest):
    """
    Function for the endpoint used to process Comms QA questions.
    """
    return process_question(req)

def process_notes_request(req: ProcessNotesRequest):
    """
    Function for the endpoint used to process advisor notes.
    """
    return process_notes(req)
