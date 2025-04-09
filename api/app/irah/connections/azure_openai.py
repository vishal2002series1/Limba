# Imports.
import os
from langchain_openai import AzureChatOpenAI, AzureOpenAI

## API Type
AZURE_OPENAI_API_TYPE = os.getenv("ZZ_AZURE_OPENAI_API_TYPE")

## Version 1 for main agent
AZURE_OPENAI_API_VERSION = os.getenv("ZZ_AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("ZZ_AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("ZZ_AZURE_OPENAI_API_KEY")

## Version 2 for financial planner
AZURE_OPENAI_B_API_VERSION = os.getenv("ZZ_AZURE_OPENAI_B_API_VERSION")
AZURE_OPENAI_B_ENDPOINT = os.getenv("ZZ_AZURE_OPENAI_B_ENDPOINT")
AZURE_OPENAI_B_API_KEY = os.getenv("ZZ_AZURE_OPENAI_B_API_KEY")

## GPT models
AZURE_OPENAI_GPT35_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_GPT35_DEPLOYMENT")
AZURE_OPENAI_GPT35_INSTRUCT_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_GPT35_INSTRUCT_DEPLOYMENT")
AZURE_OPENAI_GPT4_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_GPT4_DEPLOYMENT")
AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT =os.getenv('ZZ_AZURE_OPENAI_GPT4_TURBO_DEPLOYMENT')
AZURE_OPENAI_GTP4_32K_DEPLOYMENT = os.getenv('ZZ_AZURE_OPENAI_GTP4_32K_DEPLOYMENT')
AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT = os.getenv('ZZ_AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT')

## Models for Agents and Tools
MAIN_LLM_AGENT_MODEL = os.getenv("ZZ_MAIN_AGENT_MODEL_DEPLOYMENT") if os.getenv("ZZ_MAIN_AGENT_MODEL_DEPLOYMENT") else AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT
FINANCIAL_PLANNER_AGENT_MODEL = os.getenv("ZZ_FINANCIAL_PLANNER_TOOL_MODEL_DEPLOYMENT") if os.getenv("ZZ_FINANCIAL_PLANNER_TOOL_MODEL_DEPLOYMENT") else AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT
FP_MATH_MODEL = os.getenv("ZZ_MATH_MODEL_DEPLOYMENT") if os.getenv("ZZ_MATH_MODEL_DEPLOYMENT") else AZURE_OPENAI_GPT35_INSTRUCT_DEPLOYMENT
DATABASE_SEARCH_AGENT_MODEL = os.getenv("ZZ_DATABASE_SEARCH_TOOL_MODEL_DEPLOYMENT") if os.getenv("ZZ_DATABASE_SEARCH_TOOL_MODEL_DEPLOYMENT") else AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT
RESTRICTION_AGENT_MODEL = os.getenv("ZZ_RESTRICTION_CHECKER_TOOL_MODEL_DEPLOYMENT") if os.getenv("ZZ_RESTRICTION_CHECKER_TOOL_MODEL_DEPLOYMENT") else AZURE_OPENAI_GPT4_OMNI_DEPLOYMENT

# Initialise LLMs
## Use GPT 4 turbo as base or AZURE_OPENAI_SELECTED_MODEL
LLM = AzureChatOpenAI(
    openai_api_type = AZURE_OPENAI_API_TYPE,
    openai_api_version = AZURE_OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    openai_api_key = AZURE_OPENAI_API_KEY,
    deployment_name = MAIN_LLM_AGENT_MODEL,
    temperature = 0
)

restriction_checker_llm = AzureChatOpenAI(
    openai_api_type = AZURE_OPENAI_API_TYPE,
    openai_api_version = AZURE_OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    openai_api_key = AZURE_OPENAI_API_KEY,
    deployment_name = RESTRICTION_AGENT_MODEL,
    temperature = 0
)

database_search_llm = AzureChatOpenAI(
    openai_api_type = AZURE_OPENAI_API_TYPE,
    openai_api_version = AZURE_OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    openai_api_key = AZURE_OPENAI_API_KEY,
    deployment_name = DATABASE_SEARCH_AGENT_MODEL,
    temperature = 0
)

# Use GPT 4 for financial planner tool
financial_planner_llm = AzureChatOpenAI(
    openai_api_type = AZURE_OPENAI_API_TYPE,
    openai_api_version = AZURE_OPENAI_API_VERSION,
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    openai_api_key = AZURE_OPENAI_API_KEY,
    deployment_name = FINANCIAL_PLANNER_AGENT_MODEL,
    temperature = 0
)

# Use GPT 3.5 turbo instruct for calculator tool - math_llm
math_llm = AzureOpenAI(
    openai_api_type = AZURE_OPENAI_API_TYPE,
    openai_api_version = AZURE_OPENAI_B_API_VERSION,
    azure_endpoint = AZURE_OPENAI_B_ENDPOINT,
    openai_api_key = AZURE_OPENAI_B_API_KEY, 
    deployment_name = FP_MATH_MODEL, 
    temperature = 0
)

from openai import AzureOpenAI as AzureOpenAI_OPENAI
# Advisor Copilot
advisor_copilot_client = AzureOpenAI_OPENAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-05-15",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)
