from models.data_sources.datasource_classes import DataSource
from models.data_sources import excel


def construct_source(params: dict) -> DataSource:
    source_types = {
        'excel': excel.ExcelSource
    }
    if params['resource_type'] in source_types.keys():
        return source_types[params['resource_type']](**params)
    else:
        return None
