from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import json

connect_str = os.getenv('AZURE_COSMOS_CONNECTION_STRING')
database_name = 'testing-catalogue'
container_name = 'catalogue'
partition_key = 'catalogue_key'


client = CosmosClient.from_connection_string(connect_str)
"""
try:
    database = client.create_database(database_name)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(database_name)
"""
database = client.create_database_if_not_exists(id=database_name)
"""
try:
    container = database.create_container(id=container_name, partition_key=PartitionKey(path = '/' + partition_key))
except:
    container = database.get_container_client(container_name)
"""
container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path='/' + partition_key),
        offer_throughput=400
    )