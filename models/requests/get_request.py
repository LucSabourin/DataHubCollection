from models.data_sources.datasource_classes import DataSource
from models.catalogue.catalogue import Catalogue
from models.exceptions.exceptions import UserError,ServerError


class GETRequest():
    """
    """

    def __init__(self, catalogue_key: str, tables: list = None, fields: list = None, table_field: dict = None, field_value: dict = None, orient: str = 'records'):
        self.catalogue_key = catalogue_key
        self.tables = tables

        if fields is None:
            self.fields = []
        else:
            self.fields = fields

        if table_field is None:
            self.table_field = {}
        else:
            self.table_field = table_field

        if field_value is None:
            self.field_value = {}
        else:
            self.field_value = field_value

        self.orient = orient
        self.messages = []
        self.response_code = 0
        self.data = {}

    def process_request(self):
        success_data_source = False
        try:
            data_source = self.get_data_source()
            if self.tables is None:
                self.tables = data_source.tables
            success_data_source = True
        except UserError:
            self.response_code = 404

        if success_data_source is False:
            # Force boot if an error happened while getting DataSource
            return

        success_data = False
        try:
            self.data = self.retrieve_data(data_source)
            success_data = True
        except UserError:
            if self.messages[-1] == 88:
                self.response_code = 404
            else:    
                self.response_code = 400
        except ServerError:
            if self.messages[-1] == 89:
                self.response_code = 404
            else:    
                self.response_code = 500

        if success_data is True:
            self.response_code = 200
            for sheet in self.data:
                if len(sheet) == 0:
                    self.response_code = 204
                    break
        
        self.service_request()

    def get_data_source(self):
        return Catalogue.instance().lookup_data_source(self.catalogue_key, self.messages)

    def retrieve_data(self, data_source: DataSource):
        orients = ['split', 'records', 'index', 'columns', 'values', 'table']
        if self.orient not in orients:
            self.messages.append('98 -> Invalid orient selected for JSON format.')
            self.messages.append(98)
            raise UserError('98 -> Invalid orient selected for JSON format.')
        return data_source.get_response(
            messages=self.messages,
            tables=self.tables,
            fields=self.fields,
            table_field=self.table_field,
            field_value=self.field_value,
            orient=self.orient)

    def service_request(self):
        if len(self.messages) > 0:
            # removes severity accumulator
            self.messages.pop()
