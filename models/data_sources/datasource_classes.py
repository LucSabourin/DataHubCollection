from abc import abstractmethod, ABC
from datetime import datetime
import uuid
from io import BytesIO

from models.exceptions.exceptions import ServerError
import models.locations.specifier as spec


class DataSource(ABC):
    """Base Class for anything supplying data."""

    message_templates = {
            'connection_error': ('Could not connect to source {0}.', 99),
            'empty_row': ('There is an empty row at index {1} in source {0}.', 0),
            'empty_column': ('There is an empty column in field {1} of source {0}.', 0),
            'duplicate_keys': ('In the proposed key field {1} of source {0}, the values {2} are duplicated. Keys should be unique to each record.', 4),
            'no_such_field': ('The field {1} does not exist in source {0}.', 4),
            'no_such_value': ('The value {2} does not exist in field {1} of source {0}.', 4)
        }

    def __init__(self,
        catalogue_key: str,
        location: str = '',
        connections: list = None,
        index_fields: dict = None,
        remove_empty: bool = False,
        read_only: bool = False,
        data_fresh_date: datetime = None,
        resource_type: str = '',
        version: float = 1.0,
        metadata: dict = None,
        tags: dict = None
    ) -> None:
        self.catalogue_key = catalogue_key
        self.location = location
        if connections is not None:
            self.connections = connections
        else:
            self.connections = []

        if index_fields is not None:
            self.index_fields = index_fields
        else:
            self.index_fields = {}

        self.remove_empty = remove_empty
        self.read_only = read_only
        self.data_fresh_date = data_fresh_date
        if metadata is not None:
            self.metadata = metadata
        else:
            self.metadata = {}

        if tags is not None:
            self.tags = tags
        else:
            self.tags = {}

        self.data = {}
        self.message_severity = -1
        
    @abstractmethod
    def scan(self):
        """Builds metadata for the file which governs what processes
        be done to get the data into a provisionable asset.
        """
        pass

    @abstractmethod
    def to_dataframe(self) -> None:
        """Converts data in DataSource object to a pandas dataframe."""
        pass

    @abstractmethod
    def clean_up(self) -> None:
        """Run any necessary clean up, save logs for warnings if
        anything structurally changes or the values of data changes as
        a result.
        Ex. removing Null rows or columns.
        """
        pass

    def message(self, message_template: str, params: list, message_templates: dict) -> str:
        """
        """
        if message_template in message_templates.keys():
            if message_templates[message_template][1] > self.message_severity:
                self.message_severity = message_templates[message_template][1]
            return str(message_templates[message_template][1]) + ' -> ' + message_templates[message_template][0].format(*params)
        else:
            return f"***No matching error type found: {message_template}.***"
    
    @abstractmethod
    def get_response(self, messages: list, tables: list = None, fields: list = None, table_field: dict = None, field_value: dict = None, orient: str = 'records', **kwargs) -> dict:
        """Provides response to GET request"""
        pass

    @abstractmethod
    def serialize(self) -> dict:
        """Serializes the DataSource for storage."""
        pass



class FileSource(DataSource):
    """Class for any file-like object containing data such as json,
    csv, excel, etc.
    """

    message_templates = {
            'top_rows_empty': ('The top {1} rows of source {0} are empty and so have been omitted.', 0),
            'left_columns_empty': ('The leftmost {1} columns of source {0} are empty and so have been omitted.', 0),
            'missing_headers': ('There are missing headers in columns {1} of source {0}.', 1),
            'duplicate_headers': ('The header {1} is duplicated {2} times in columns {3} in source {0}.', 1),
            'hierarchical_headers': ('The hierarchical headers {1} in file {0} have been combined into a single header, with <.> separating each layer (top layer on the left and bottom layer on the right).', 1),
            'could_not_load_into_pandas': ('The data from source {0} could not be loaded into pandas for analysis.', 99)
        }

    def __init__(self,
        catalogue_key: str,
        location: str = '',
        connections: list = None,
        index_fields: dict = None,
        remove_empty: bool = False,
        read_only: bool = False,
        data_fresh_date: datetime = None,
        ingested_location: str = '',
        ingested_at: str = '',
        ingested: bool = False,
        resource_type: str = '',
        version: float = 1.0,
        metadata: dict = None,
        file_name: str = '',
        location_type: str = '',
        tags: dict = None
    ) -> None:
        DataSource.__init__(self,
            catalogue_key=catalogue_key,
            location=location,
            connections=connections,
            index_fields=index_fields,
            remove_empty=remove_empty,
            read_only=read_only,
            data_fresh_date=data_fresh_date,
            resource_type=resource_type,
            version=version,
            metadata=metadata,
            tags=tags
        )
        self.ingested_location = ingested_location
        self.ingested_at = ingested_at
        self.ingested = ingested
        self.updating = True
        self.file_name = file_name
        self.file = None
        self.location_type = location_type

    def ingest_oc_file(self, location: str, messages: list) -> None:
        """Returns Jsonified dict of error messages above threshold
        (yet to be integrated - for now all possible messages), if any.
        """
        self.file_name = location.split('/')[4:]
        self.location = location
        self.location_type = spec.evalutate_type(location)
        
        self.get_file(location, messages)
        self.scan(messages)
        self.to_dataframe(messages)
        self.clean_up(messages)

        if len(messages) > 0:
            messages.append(self.message_severity)

    def store_oc_file(self, messages: list) -> None:
        self.store_oc_data(messages=messages)
        self.delete_file(self.location, messages)
        self.location = ''

    def store_oc_data(self, messages: list) -> None:
        """
        """
        pass

    def retrieve_data(self, tables: list, messages: list) -> None:
        """
        """
        pass

    def delete_response(self) -> None:
        """
        """
        pass

    def message(self, message_template: str, params: list, message_templates: dict) -> str:
        """
        """
        if message_template in message_templates.keys():
            if message_templates[message_template][1] > self.message_severity:
                self.message_severity = message_templates[message_template][1]
            return str(message_templates[message_template][1]) + ' -> ' + message_templates[message_template][0].format(*params)
        else:
            return super().message(message_template, params, super().message_templates)
    
    def get_file(self, location: str, messages: list) -> BytesIO:
        try:
            contents = spec.get_file(location=location, location_type=self.location_type)
        except ServerError as msg:
            messages.append(msg.message)
            # Assign severity
            messages.append(int(msg.message.split(' -> ')[0]))
            raise ServerError(msg.message)
        
        if location[-5:] != '.json':
            self.file = contents
            self.updating = True
        else:
            return contents

    def assign_folder(self, messages: list) -> str:
        while True:
            folder = str(uuid.uuid4())
            try:
                folder_exists = spec.file_exists(location=folder + '/:ingested.json', location_type=self.location_type)
            except ServerError as msg:
                messages.append(msg.message)
                # Assign severity
                messages.append(int(msg.message.split(' -> ')[0]))
                raise ServerError(msg.message)
            else:
                if folder_exists is False:
                    return folder
    
    def post_file(self, file_name: str, data: dict, messages: list, tags: dict, old_url: str = '') -> str:
        """
        """
        try:
            url = spec.post_file(file_name=file_name, contents=data, tags=tags, location_type=self.location_type)
        except ServerError as msg:
            messages.append(msg.message)
            # Assign severity
            messages.append(int(msg.message.split(' -> ')[0]))
            raise ServerError(msg.message)
        else:
            if len(old_url) > 0:
                try:
                    self.delete_file(location=old_url, messages=messages)
                except ServerError as msg:
                    raise ServerError(msg)
        return url

    def delete_file(self, location: str, messages: list) -> None:
        try:
            spec.delete_file(location=location, location_type=self.location_type)
        except ServerError as msg:
            messages.append(msg.message)
            # Assign severity
            messages.append(int(msg.message.split(' -> ')[0]))
            raise ServerError(msg.message)

    def failed_clean_up(self, messages: list) -> None:
        """
        """
        pass


class SqlSource(DataSource):
    """Class for any SQL-like object containing data such as mysql,
    sql-server, nosql, etc.
    """

    pass
