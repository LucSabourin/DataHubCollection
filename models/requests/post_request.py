import json

from models.data_sources.datasource_classes import DataSource
from models.constructors.data_source_constructor import construct_source
from models.catalogue.catalogue import Catalogue
from models.exceptions.exceptions import UserError, ServerError


class POSTRequest():
    """
    """
    
    def __init__(self, location: str, source_params: dict, proposed_key: str, error_threshold: int = -1, tags: dict = None):
        self.location = location
        self.source_params = source_params
        self.proposed_key = proposed_key
        self.error_threshold = error_threshold
        self.tags = tags
        self.messages = []
        self.response_code = 0
        self.catalogue_key = ''

    def process_request(self):
        success = False
        self.reserved_key = Catalogue.instance().reserve_key(self.proposed_key)
        self.source_params['catalogue_key'] = self.reserved_key
        try:
            data_source = self.process_data_source()
            success = True
        except UserError:
            self.response_code = 400
        except ServerError:
            if self.messages[-1] == 89:
                self.response_code = 404
            else:
                self.response_code = 500

        if success is True:
            self.catalogue_key = self.register_with_catalogue(data_source)
            self.response_code = 201
        else:
            Catalogue.instance().unreserve_key(self.reserved_key)
        
        self.service_request()

    def process_data_source(self) -> DataSource:
        pass

    def register_with_catalogue(self, data_source: DataSource) -> str:
        return Catalogue.instance().register_data_source(data_source, self.reserved_key, self.tags)

    def service_request(self):
        if len(self.messages) > 0:
            # removes severity accumulator
            self.messages.pop()


class POSTFileRequest(POSTRequest):
    """
    """
    def __init__(self, location: str, source_params: dict, proposed_key: str, error_threshold: int = -1, tags: dict = None):
        POSTRequest.__init__(self, location, source_params, proposed_key, error_threshold, tags)

    def process_data_source(self) -> DataSource:
        data_source = construct_source(self.source_params)
        try:
            data_source.ingest_oc_file(self.location, messages=self.messages)
        except UserError as msg:
            raise UserError(msg)
        except ServerError as msg:
            raise ServerError(msg)
        else:
            if len(self.messages) > 0:
                if self.messages[-1] > self.error_threshold:
                    raise UserError('97 -> Severity of errors exceeded user error tolerance.')

        try:
            data_source.store_oc_file(messages=self.messages)
        except UserError as msg:
            data_source.failed_clean_up(messages=self.messages)
            raise UserError(msg)
        except ServerError as msg:
            data_source.failed_clean_up(messages=self.messages)
            raise ServerError(msg)
        else:
            if len(self.messages) > 0:
                if self.messages[-1] > self.error_threshold:
                    raise UserError('97 -> Severity of errors exceeded user error tolerance.')

        return data_source
            
    
