from azure.cosmos import CosmosClient,PartitionKey

def post_to_cosmos(connect_str: str, database_name: str, container_name: str, catalogue_key: str, data: dict):
    """
    """
    client = CosmosClient.from_connection_string(conn_str=connect_str)
    database = client.get_database_client(database=database_name)
    container = database.get_container_client(container=container_name)
    data['catalogue_key'] = catalogue_key
    data['id'] = catalogue_key
    container.create_item(body=data)

def get_from_cosmos(connect_str: str, database_name: str, container_name: str, catalogue_key: str = None):
    """
    """
    client = CosmosClient.from_connection_string(conn_str=connect_str)
    database = client.get_database_client(database=database_name)
    container = database.get_container_client(container=container_name)
    if catalogue_key is not None:
        query = "SELECT * FROM c WHERE c.catalogue_key IN('{0}')".format(catalogue_key)
    else:
        query = "SELECT * FROM c"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    returns = {}
    for item in items:
        if 'catalogue_key' in item.keys():
            returns[item['catalogue_key']] = [item, None]
            returns[item['catalogue_key']][0].pop('id')
            returns[item['catalogue_key']][0].pop('catalogue_key')
    return returns

def update_item_in_cosmos(connect_str: str, database_name: str, container_name: str, catalogue_key: str, data: dict):
    """
    """
    client = CosmosClient.from_connection_string(conn_str=connect_str)
    database = client.get_database_client(database=database_name)
    container = database.get_container_client(container=container_name)
    query = "SELECT * FROM c WHERE c.catalogue_key IN('{0}')".format(catalogue_key)
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        data['catalogue_key'] = catalogue_key
        container.replace_item(item=item, body=data, populate_query_metrics=None, pre_trigger_include=None, post_trigger_include=None)

def check_catalogue_key_exists(connect_str: str, database_name: str, container_name: str, catalogue_key: str):
    """
    """
    client = CosmosClient.from_connection_string(conn_str=connect_str)
    database = client.get_database_client(database=database_name)
    container = database.get_container_client(container=container_name)
    query = "SELECT * FROM c WHERE c.catalogue_key IN('{0}')".format(catalogue_key)
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return bool(len(items) > 0)
