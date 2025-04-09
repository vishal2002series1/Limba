# Imports
import os

from azure.storage.blob import BlobServiceClient

# Get environment variables
AZURE_BLOB_CONNECTION_STRING = os.getenv("ZZ_AZURE_STORAGE_CONNECTION_STRING")
AZURE_BLOB_CONTAINER_NAME = os.getenv("ZZ_AZURE_STORAGE_CONTAINER")
AZURE_BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
AZURE_CONTAINTER_CLIENT = AZURE_BLOB_SERVICE_CLIENT.get_container_client(AZURE_BLOB_CONTAINER_NAME)