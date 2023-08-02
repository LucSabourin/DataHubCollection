from models.data_sources.datasource_classes import DataSource
from models.constructors.data_source_constructor import construct_source
import uuid
import json
import threading

import os
from models.exceptions.exceptions import UserError
### Until cosmos db/NOSQL testing is done.
from models.connections import blob

### Cosmos db testing in progress.
from models.connections import cosmosdb

class Catalogue():

    ### Until cosmos db/NOSQL testing is done.
    __container = 'testing-catalogue'
    __file_name = 'catalogue.json'
    
    ### Cosmos db testing in progress.
    #__connect_str = os.getenv('AZURE_COSMOS_CONNECTION_STRING')
    #__db_name = 'testing-catalogue'
    #__container = 'catalogue'
    #__partition_key = 'catalogue_key'
    
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def __init__(self):
        self.deserialize()

    @classmethod
    def instance(Catalogue):
        if Catalogue.__singleton_instance is None:
            with Catalogue.__singleton_lock:
                if Catalogue.__singleton_instance is None:
                    Catalogue.__singleton_instance = Catalogue()
        return Catalogue.__singleton_instance

    def reserve_key(self, key: str) -> str:
        catalogue_key = key
        while True:
            if catalogue_key not in self.catalogue.keys():
                self.catalogue[catalogue_key] = []
                return catalogue_key
            else:
                catalogue_key = key + '-' + str(uuid.uuid4())[0:4]

    def unreserve_key(self, key: str) -> None:
        if key in self.catalogue.keys():
            self.catalogue.pop(key)

    def register_data_source(self, data_source: DataSource, key: str, tags: dict = None) -> str:
        catalogue_key = key
        if self.catalogue[key] != []:
            catalogue_key += '-' + str(uuid.uuid4())[0:4]
            
        serialized = json.loads(json.dumps(data_source.serialize()))
        if tags is not None:
            serialized['tags'] = tags
        self.catalogue[catalogue_key] = [serialized, data_source]
        self.serialize()
        return catalogue_key

    def update_data_source(self, data_source: DataSource, key: str) -> None:
        if key in self.catalogue.keys() is True:
            serialized = json.loads(json.dumps(data_source.serialize()))
            self.catalogue[key] = serialized

    def lookup_data_source(self, key: str, messages: list) -> DataSource:
        if key in self.catalogue.keys():
            if self.catalogue[key][1] is None:
                data_source_params = self.catalogue[key][0]
                data_source = construct_source(data_source_params)
                self.catalogue[key][1] = data_source
                return data_source
            else:
                return self.catalogue[key][1]
        else:
            messages.append(f'88 -> No key in catalogue found matching {key}')
            messages.append(88)
            raise UserError(f'88 -> No key in catalogue found matching {key}')

    def delete_data_source(self, key: str, messages: list) -> None:
        if key in self.catalogue.keys():
            self.catalogue.pop(key)
            self.serialize()
        else:
            messages.append(f'88 -> No key in catalogue found matching {key}')
            messages.append(88)
            raise UserError(f'88 -> No key in catalogue found matching {key}')
    
    def serialize(self) -> None:
        ### BLOB STORAGE
        serialized = {}
        for key, data_source in self.catalogue.items():
            serialized[key] = [data_source[0], None]
        if blob.check_blob_exists(location=self.__file_name, container=self.__container) is True:
            blob.post_file_to_blob(container=self.__container, file_name='temp/' + self.__file_name, contents=json.dumps(serialized))
            blob.delete_file_from_blob(location=self.__file_name, container=self.__container)
            blob.post_file_to_blob(container=self.__container, file_name=self.__file_name, contents=json.dumps(serialized))
            blob.delete_file_from_blob(location='temp/' + self.__file_name, container=self.__container)
        else:    
            blob.post_file_to_blob(container=self.__container, file_name=self.__file_name, contents=json.dumps(serialized))

        """### COSMOS
        for key, data_source in self.catalogue.items():
            cosmosdb.post_to_cosmos(self.__connect_str, self.__db_name, self.__container, catalogue_key=key, data=data_source[0])
        """

    def delete_catalogue(self) -> None:
        blob.delete_file_from_blob(location=self.__file_name, container=self.__container)

    def deserialize(self) -> None:
        ### BLOB STORAGE
        if blob.check_blob_exists(location=self.__file_name, container=self.__container):
            self.catalogue = json.load(blob.get_file_from_blob(location=self.__file_name, container=self.__container))
        else:
            self.catalogue = {}

        """
        ### COSMOS
        self.catalogue = {}
        catalogue = cosmosdb.get_from_cosmos(self.__connect_str, self.__db_name, self.__container)
        if len(catalogue.keys()) > 0:
            self.catalogue = catalogue
        """
