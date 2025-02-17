from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import csv
import pandas as pd

def get_blob_service_client_sas():
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://asrcadataextract.blob.core.windows.net/?"
    # The SAS token string can be assigned to credential here or appended to the account URL
    credential = "sv=2022-11-02&ss=bfq&srt=sco&sp=rwlacupiytfx&se=2025-03-29T20:21:22Z&st=2024-09-26T12:21:22Z&spr=https&sig=aX3soRD1z2RuCFeDI5Y9u92Oq2Bm1%2FzwToRNwv7zI98%3D"

    # Create the BlobServiceClient object
    #blob_service_client = BlobServiceClient(account_url)
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    return blob_service_client

blob = get_blob_service_client_sas()

def list_blobs_flat(blob_service_client: BlobServiceClient, container_name):
    container_client = blob_service_client.get_container_client(container=container_name)

    blob_list = container_client.list_blobs()
    print("blobs:")
    for blob in blob_list:
        #if blob.name == 'EAR_Current_Status.csv':
        if blob.name == 'EAR_Current_Status.csv':
            print(f"Name: {blob.name}")
            blob_client = container_client.get_blob_client(blob.name)
            this_csv = pd.read_csv(blob_client.download_blob())            
            print(this_csv.head())


def list_containers(blob_service_client: BlobServiceClient):
    containers = blob_service_client.list_containers(include_metadata=True)
    print("containers:")
    for container in containers:
        #print(container['name'], container['metadata'])
        list_blobs_flat(blob,container)

list_containers(blob)



