import os
os.environ["AZURESEARCH_FIELDS_ID"] = "content_id"
os.environ["AZURESEARCH_FIELDS_CONTENT"] = "content"
os.environ["AZURESEARCH_FIELDS_CONTENT_VECTOR"] = "content_embedding"

from langchain.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

AZURE_OPENAI_API_TYPE = os.getenv("ZZ_AZURE_OPENAI_API_TYPE")
AZURE_OPENAI_API_VERSION = os.getenv("ZZ_AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("ZZ_AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("ZZ_AZURE_OPENAI_API_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("ZZ_AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

AZURE_AI_SEARCH_ENDPOINT = os.getenv("ZZ_AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_QUERY_KEY = os.getenv("ZZ_AZURE_AI_SEARCH_ADMIN_KEY")
AZURE_AI_SEARCH_INDEX = os.getenv("ZZ_AZURE_AI_SEARCH_INDEX")

EMBEDDING_MODEL: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    openai_api_type=AZURE_OPENAI_API_TYPE,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    chunk_size=1
)

VECTOR_STORE: AzureSearch = AzureSearch(
    azure_search_endpoint=AZURE_AI_SEARCH_ENDPOINT,
    azure_search_key=AZURE_AI_SEARCH_QUERY_KEY,
    index_name=AZURE_AI_SEARCH_INDEX,
    embedding_function=EMBEDDING_MODEL.embed_query,
)