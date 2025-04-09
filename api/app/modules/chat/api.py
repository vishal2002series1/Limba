# Imports
from fastapi import APIRouter, Depends
from datetime import datetime

from app.irah.router import IRAH_APIRoute
from . import schema, actions
from app.modules.auth.actions import verify_password as security
from app.modules.auth.schema import AuthSchema
from app.irah.connections import LLM, financial_planner_llm
from .tools.FinancialPlannerTool import financial_planner_chat_agent
from app.irah.logs import logger


# Instantiate router
router = APIRouter(route_class=IRAH_APIRoute)
router1 = APIRouter(route_class=IRAH_APIRoute)
advisor_copilot = APIRouter()

# Main chat agent endpoint
@router.post("")
def custom_chat(req: schema.CustomChatRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint is used for the main chat agent. It uses the default settings for the chat agent, excluding only the GoogleSearchTool.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# Custom Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# Custom Chat end #################")

    return response.model_dump(exclude_none=True)


# Wealth chat agent endpoint
@router.post("/wealth")
def wealth_chat(req: schema.WealthChatRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint is used for the wealth chat agent. It uses the default settings for the chat agent, excluding investment recommendation and market activity restrictions.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# Wealth Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.wealth_agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# Wealth Chat end #################")

    return response.model_dump(exclude_none = True)

@router.post("/financial_planner")
def financial_planner_chat(req: schema.FinancialPlannerAgentRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint is used for the financial planner chat agent endpoint / UI.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# FinancialPlanner Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.financial_planner_agent(llm = financial_planner_llm, req = req)
    logger.info(f"[{datetime.now()}]  ################# FinancialPlanner Chat end #################")

    return response.model_dump(exclude_none = True)


@router.post("/financial_planner_test")
def financial_planner_chat_test(req: schema.FinancialPlannerChatRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint is used for the financial planner chat agent endpoint / UI. It was a  test endpoint for the financial planner chat agent.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# FinancialPlanner Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = financial_planner_chat_agent(llm = financial_planner_llm, req = req)
    logger.info(f"[{datetime.now()}]  ################# FinancialPlanner Chat end #################")

    return response["output"]


# ESG chat agent endpoint
@router.post("/esg")
def esg_chat(req: schema.WealthChatRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint was used for an ESG demo. It only queries specifically uploaded ESG documents.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# ESG Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.esg_agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# ESG Chat end #################")

    return response.model_dump(exclude_none = True)


# Trust chat agent endpoint
@router.post("/trust_review")
def trust_chat(req: schema.WealthChatRequest, identity:AuthSchema = Depends(security)):
    """
    This API endpoint was used for a trust review demo. It only queries specifically uploaded trust review documents.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# Trust Review Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.trust_agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# Trust Review Chat end #################")

    return response.model_dump(exclude_none = True)


# Unrestricted chat agent endpoint
@router.post("/unrestricted")
def unrestricted_chat(req: schema.CustomChatRequest, identity:AuthSchema = Depends(security)):
    """"
    This chat endpoint is a free for all chat endpoint to show the full  unrestricted capabilities of the IRAH chat agent.
    It does not have any restrictions and includes all the available tools in the IRAH chat agent.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# Unrestricted Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.unrestricted_agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# Unrestricted Chat end #################")

    return response.model_dump(exclude_none = True)


# PE Pension demo chat agent endpoint
@router.post("/pe_pension_demo")
def pe_pension_demo_chat(req: schema.CustomChatRequest, identity:AuthSchema = Depends(security)):
    """
    This chat endpoint is a demo chat endpoint for the a Private Equity Pension Plan chat agent for a healthcare client.
    It uses the default settings for the chat agent, excluding only the FinancialPlannerTool.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# HOOPP Demo Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.pe_pension_demo_agent_search(llm = LLM, req = req)
    logger.info(f"[{datetime.now()}]  ################# HOOPP Demo Chat end #################")

    return response.model_dump(exclude_none = True)


# Endpoint for getting the files from storage
@router1.post("/get_documents")
def get_documents(item: schema.GetDocsSchema, identity:AuthSchema = Depends(security)):
    file = actions.get_blob_docs(item.path, item.filename)
    return file



# advisor_copilot

@advisor_copilot.post("/process_question")
def api_process_question(req: schema.CombinedQuestionRequest):
    """
    This API endpoint is used for the advisor copilot comms search agent.
    """
    # Log API start and request
    logger.info(f"[{datetime.now()}]  ################# Advisor Copilot Chat start #################")
    logger.info(f"[{datetime.now()}]  api - request: {req}")

    # Get response from the chat agent and log API end
    response = actions.process_question(req)
    logger.info(f"[{datetime.now()}]  ################# Advisor Copilot Chat end #################")

    return response.model_dump(exclude_none=True)

@advisor_copilot.post("/process_notes")
def api_process_notes(req: schema.ProcessNotesRequest):
    """
    This API endpoint is used for processing notes.
    """
    # Log API start
    logger.info(f"[{datetime.now()}]  ################# Process Notes start #################")

    # Get response from the notes processor and log API end
    response = actions.process_notes(req)
    logger.info(f"[{datetime.now()}]  ################# Process Notes end #################")

    return response.model_dump(exclude_none=True)