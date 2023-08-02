import os, re
from models.connections import blob

location_types = {
    'blob.core.windows.net': 'blob',
    'database.windows.net': 'sql',
    None: 'local'
}
get_file_types = {
    'blob': blob.get_file_from_blob,
    'local': None
}
file_exists_types = {
    'blob': blob.check_blob_exists,
    'local': None
}
post_file_types = {
    'blob': blob.post_file_to_blob,
    'local': None
}
delete_file_types = {
    'blob': blob.delete_file_from_blob,
    'local': None
}

def evalutate_type(location: str):
    for key in location_types.keys():
        if key is None:
            if 'http' != location[0:4]:
                return location_types[key]
        else:
            if key in location:
                return location_types[key]

def get_file(location: str, location_type: str):
    func = get_file_types[location_type]
    return func(location=location)

def post_file(file_name: str, contents, tags: dict = None, location_type: str = 'blob'):
    func = post_file_types[location_type]
    return func(file_name=file_name, contents=contents, tags=tags)

def file_exists(location: str, location_type: str):
    func = file_exists_types[location_type]
    return func(location=location)

def delete_file(location: str, location_type: str):
    func = delete_file_types[location_type]
    return func(location=location)
