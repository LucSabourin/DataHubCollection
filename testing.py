from testing_reset import reset_testing

from models.catalogue.catalogue import Catalogue
from models.constructors.request_constructor import construct_post_request, construct_get_request, construct_delete_request

test = False

def chess_data():
    local_path = 'Testing/Chess/chess_games_rawonly.xlsx'
    
    post_params = {}
    post_params['location'] = reset_testing(local_path=local_path)
    post_params['source_params'] = {'resource_type': 'excel', 'tables': []}
    post_params['error_threshold'] = 0
    post_params['proposed_key'] = 'TestingChess'
    post_params['tags'] = {'testing': 'chess'}

    get_params = {}
    #get_params['tables'] = []
    #get_params['fields'] = []
    #get_params['field_value'] = {}
    get_params['orient'] = 'records'

    return {'post': post_params, 'get': get_params}

def good_data():
    local_path = 'Testing/Good/Testing.xlsx'
    
    post_params = {}
    post_params['location'] = reset_testing(local_path=local_path)
    post_params['source_params'] = {'resource_type': 'excel', 'tables': ['Sheet2','TestSheet']}
    post_params['error_threshold'] = 0
    post_params['proposed_key'] = 'TestingGood'
    post_params['tags'] = {'testing': 'good'}

    get_params = {}
    #get_params['tables'] = []
    #get_params['fields'] = []
    #get_params['field_value'] = {}
    get_params['orient'] = 'records'

    return {'post': post_params, 'get': get_params}

def bad_data():
    local_path = 'Testing/Bad/TestingBad.xlsx'
    
    post_params = {}
    post_params['location'] = reset_testing(local_path=local_path)
    post_params['source_params'] = {'resource_type': 'excel', 'tables': ['Sheet3','Sheet5','Sheet8','TestSheet']}
    post_params['error_threshold'] = 10
    post_params['proposed_key'] = 'TestingBad'
    post_params['tags'] = {'testing': 'bad'}

    get_params = {}
    get_params['tables'] = ['Sheet3','Sheet5','Sheet8','TestSheet']
    #get_params['fields'] = ['Field2']
    #get_params['field_value'] = {'Field2': 300}
    get_params['orient'] = 'records'

    return {'post': post_params, 'get': get_params}

def post_testing(post_params: dict):
    request = construct_post_request(post_params)
    request.process_request()

    print([request.catalogue_key, request.messages, request.response_code])
    print('Post Successful!')
    print('')

    return request.catalogue_key

def get_testing(get_params: dict, key: str):
    get_params['catalogue_key'] = key
    
    request = construct_get_request(get_params)
    request.process_request()

    print([request.data, request.messages, request.response_code])
    print('Get Successful!')
    print('')

def delete_testing(key):
    delete_params = {}
    delete_params['catalogue_key'] = key
    
    request = construct_delete_request(delete_params)
    request.process_request()

    print('Delete Successful!')
    print('')

if __name__ == '__main__':
    params = chess_data()
    #params = good_data()
    #params = bad_data()

    if test == True:
        catalogue = Catalogue.instance()
        key = post_testing(params['post'])

        catalogue.serialize()
        catalogue = Catalogue.instance()
        get_testing(params['get'], key)
        delete_testing(key)