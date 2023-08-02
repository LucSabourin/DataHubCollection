from io import BytesIO
import json, os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


from models.data_sources import excel
from models.connections import blob

print(str(uuid.uuid4()))
"""
try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = 'testing-python'
    if container_name in blob_service_client.list_containers():
        print('Container Already Exists')
        container_client = blob_service_client.get_container_client(container_name)
    else:
        print('Making New Container')
        container_client = blob_service_client.create_container(container_name)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    source = '/'.join([ROOT_DIR, 'Testing/Bad/TestingBad.xlsx'])
    blob_client = blob_service_client.get_blob_client(container=container_name,blob='TestingBad.xlsx')
    print("\nUploading to Azure Storage as blob:\n\t" + 'Testing - Bad.json')
    with open(source, "rb") as data:
        blob_client.upload_blob(data)

    print("\nListing blobs...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Quick start code goes here

except Exception as ex:
    print('Exception:')
    print(ex)

#print(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
"""