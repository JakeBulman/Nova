from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def get_blob_service_client_sas():
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://ciermassessor.blob.core.windows.net/?"
    # The SAS token string can be assigned to credential here or appended to the account URL
    credential = "sv=2022-11-02&ss=b&srt=s&sp=rlc&se=2027-07-05T20:40:03Z&st=2024-04-12T12:40:03Z&spr=https&sig=KcCINWo9X8%2BdhkOJQSffyz2l5BBIXgWY%2FyPehvbJgpI%3D"

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
        print(f"Name: {blob.name}")

def list_containers(blob_service_client: BlobServiceClient):
    containers = blob_service_client.list_containers(include_metadata=True)
    print("containers:")
    for container in containers:
        print(container['name'], container['metadata'])
        list_blobs_flat(blob,container)

list_containers(blob)



