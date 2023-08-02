import json

from models.data_sources.datasource_classes import DataSource
from models.catalogue.catalogue import Catalogue
from models.exceptions.exceptions import UserError,ServerError

import os


class DELETERequest():
    """
    """

    def __init__(self, catalogue_key: str):
        self.catalogue_key = catalogue_key
        self.messages = []
        self.response_code = 0

    def process_request(self):
        success_data_source = False
        try:
            data_source = self.get_data_source()
            success_data_source = True
        except UserError:
            self.response_code = 400

        if success_data_source is False:
            # Force boot if an error happened while getting DataSource
            return
        
        success_data = False
        try:
            self.data = self.delete_data(data_source)
            success_data = True
        except UserError:
            self.response_code = 400
        except ServerError:
            self.response_code = 500
        
        if success_data is True:
            self.response_code = 204
            Catalogue.instance().delete_data_source(key=self.catalogue_key, messages=self.messages)
        self.service_request()

    def get_data_source(self):
        return Catalogue.instance().lookup_data_source(self.catalogue_key, self.messages)

    def delete_data(self, data_source: DataSource):
        data_source.delete_response(messages=self.messages)

    def service_request(self):
        if len(self.messages) > 0:
            # removes severity accumulator
            self.messages.pop()
