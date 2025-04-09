from azure.storage.blob import BlobServiceClient, __version__
from datetime import datetime, timedelta
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions, ContentSettings
import os

class blobUrl():

    def __init__(self) -> None:
         pass

    def blob_sas_token(container_client, Container, storage_account_name, storage_account_key, file_name):
        sas_url = None
        try:
            azure_folder_list = []

            # List all blobs and gather unique folder names
            for blob in container_client.list_blobs():
                folder_name = blob.name.split('/')[0]
                if folder_name not in azure_folder_list:
                    azure_folder_list.append(folder_name)

            # Iterate through each folder and generate SAS token if the blob exists
            for azure_folder_name in azure_folder_list:
                file_path_on_azure = os.path.join(azure_folder_name, file_name)
                blob_client = container_client.get_blob_client(file_path_on_azure)
                content_settings = ContentSettings(content_type="application/pdf", content_disposition="inline")
                
                try:
                    if blob_client.exists():
                        print(file_path_on_azure)
                        sas = generate_blob_sas(account_name=storage_account_name,
                                                account_key=storage_account_key,
                                                container_name=Container,
                                                blob_name=azure_folder_name + "/" + file_name,
                                                permission=BlobSasPermissions(read=True),
                                                content_disposition=content_settings.content_disposition,
                                                expiry=datetime.utcnow() + timedelta(days=1000)
                                                )

                        sas_url = f'https://{storage_account_name}.blob.core.windows.net/{Container}/{azure_folder_name}/{file_name}?{sas}'
                        print("sas url...........................", sas_url)
                except Exception as e:
                    logger.exception(f"Error checking blob existence or generating SAS for {file_path_on_azure}: {e}")
                    
        except Exception as e:
            logger.exception(f"Error listing blobs or generating SAS token: {e}")
        return sas_url
