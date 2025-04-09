import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from azure.search.documents import SearchClient

DOTENV_FILEPATH = os.path.join('.env')
DEV_ENV = os.path.exists(DOTENV_FILEPATH)
print("DEV ENV: ", DEV_ENV)
if DEV_ENV:
    print("LOADING ENV VARIABLES...")
    load_dotenv(DOTENV_FILEPATH, override=True)

# try:
AZURE_OPENAI_API_TYPE = os.getenv("ZZ_AZURE_OPENAI_API_TYPE")
AZURE_OPENAI_API_VERSION = os.getenv("ZZ_AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("ZZ_AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("ZZ_AZURE_OPENAI_API_KEY")
AZURE_OPENAI_GPT35_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_GPT35_DEPLOYMENT")
AZURE_OPENAI_GPT4_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_GPT4_DEPLOYMENT")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

AZURE_DI_ENDPOINT = os.getenv("ZZ_AZURE_DI_ENDPOINT")
AZURE_DI_KEY = os.getenv("ZZ_AZURE_DI_KEY")
AZURE_DI_MODEL_ID = os.getenv("ZZ_AZURE_DI_MODEL_ID")

AZURE_AI_SEARCH_ENDPOINT = os.getenv("ZZ_AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_ADMIN_KEY = os.getenv("ZZ_AZURE_AI_SEARCH_ADMIN_KEY")
AZURE_AI_SEARCH_INDEX = os.getenv("ZZ_AZURE_AI_SEARCH_INDEX")
# except Exception as e:
#     print(f"Error loading environment variables: {e}")

# Initialize LLM
# try:
LLM = AzureChatOpenAI(
    openai_api_type=AZURE_OPENAI_API_TYPE,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY,
    deployment_name=AZURE_OPENAI_GPT35_DEPLOYMENT,
    temperature=0
)
# except Exception as e:
#     print(f"Error initializing AzureChatOpenAI: {e}")

# Initialize Embedding Model
# try:
EMBEDDING_MODEL = AzureOpenAIEmbeddings(
    openai_api_type=AZURE_OPENAI_API_TYPE,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT
)
# except Exception as e:
#     print(f"Error initializing AzureOpenAIEmbeddings: {e}")

# Initialize Document Analysis Client
# try:
DOC_INTEL_CLIENT = DocumentAnalysisClient(
    endpoint=AZURE_DI_ENDPOINT, credential=AzureKeyCredential(AZURE_DI_KEY)
)
# except Exception as e:
#     print(f"Error initializing DocumentAnalysisClient: {e}")

# Initialize Search Client
# try:
AI_SEARCH_CLIENT = SearchClient(
    endpoint=AZURE_AI_SEARCH_ENDPOINT,
    index_name=AZURE_AI_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_AI_SEARCH_ADMIN_KEY)
)
# except Exception as e:
#     print(f"Error initializing SearchClient: {e}")
