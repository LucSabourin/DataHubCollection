import os
from io import BytesIO

from models.connections import blob

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container = 'testing-python'
blob_bad = 'Testing/Bad/TestingBad.xlsx'
blob_good = 'Testing/Good/Testing.xlsx'
file_bad = '/'.join([ROOT_DIR, 'Testing/Bad/TestingBad.xlsx'])
file_good = '/'.join([ROOT_DIR, 'Testing/Good/Testing.xlsx'])

with open(file_bad, 'r') as bad:
    blob.send_file_to_blob(connect_str, container, blob_bad, bad)

with open(file_good, 'r') as good:
    blob.send_file_to_blob(connect_str, container, blob_good, good)