import os

from models.catalogue.catalogue import Catalogue
from models.connections import blob

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def reset_testing(local_path: str):
    file_name = local_path.split('/')[-1]
    blob.delete_file_from_blob(location=file_name, container='ingestionsource')
    Catalogue.instance().delete_catalogue()

    source = '/'.join([ROOT_DIR, local_path])

    with open(source, 'rb') as data:
        local_url = blob.post_file_to_blob(file_name=file_name, contents=data,container='ingestionsource')

    return local_url