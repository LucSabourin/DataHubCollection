import os
from flask import Flask
from flask import request,jsonify
from datetime import datetime
#from models.constructors.request_constructor import construct_post_request, construct_get_request

from models.constructors.request_constructor import construct_get_request
from models.constructors.request_constructor import construct_post_request
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/catlg/<key>', methods = ['POST','GET'])
def catalog(key):
    if request.method == 'GET':
        connect_str_storage = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container = 'ingestionsource'
        sought_key = key
        params_1 = {'resource_type': 'excel'}
        file_1 = {'connect_str': connect_str_storage, 'container': container, 'blob_name': request.args.get('source')}
        tags_1 = {'catalogkey': sought_key}

        get_params_1 = {'catalogue_key':sought_key}
        request_1 = construct_get_request(get_params_1)
        request1Data = request_1.process_request()
        response = {}
        if len(request_1.messages) > 0:
            response['message'] = request_1.messages
        response['data'] = request_1.data
        return jsonify(**response), request_1.response_code

        return 200
    if request.method == 'POST':
        connect_str_storage = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container = 'ingestionsource'
        proposed_key = key
        params_1 = {'resource_type': 'excel'}
        file_1 = {'connect_str': connect_str_storage, 'container': container, 'blob_name': request.args.get('source')}
        tags_1 = {'catalogkey': proposed_key}

        account = os.getenv('BLOB_STORAGE_ACCOUNT')
        account_url = f'https://{account}.blob.core.windows.net'
        credential_key = os.getenv('BLOB_STORAGE_KEY')
        store_container = 'testing-python'
        ingest_container = 'ingestionsource'
        location = account_url+'/'+ingest_container+'/'+request.args.get('source')

        post_params_1 = {'location': location, 'source_params': params_1, 'proposed_key': proposed_key, 'tags': tags_1}
        request_1 = construct_post_request(post_params_1)
        request1Data = request_1.process_request()
        response = {}
        if len(request_1.messages) > 0:
            response['message'] = request_1.messages
        response['data'] = request_1.catalogue_key
        return jsonify(**response), request_1.response_code

@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    #match_object = re.match("[a-zA-Z]+", name)

    #if match_object:
    #    clean_name = match_object.group(0)
    #else:
    #    clean_name = "Friend"

    content = "Hello there, " + name + "! It's " + formatted_now
    return content

app.run(port=5000, debug=True)