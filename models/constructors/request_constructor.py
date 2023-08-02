from models.requests.get_request import GETRequest
from models.requests.delete_request import DELETERequest
from models.requests.post_request import POSTRequest, POSTFileRequest

def construct_post_request(params: dict) -> POSTRequest:
    post_request_types = {
        'excel': POSTFileRequest
    }
    check = check_layer(params, 'resource_type')
    if check[0] is True:
        for key in post_request_types.keys():
            if key == check[1]:
                return post_request_types[key](**params)

def construct_get_request(params: dict) -> GETRequest:
    return GETRequest(**params)

def construct_delete_request(params: dict) -> DELETERequest:
    return DELETERequest(**params)

def check_layer(params: dict, match) -> tuple:
    if match in params.keys():
        return (True, params[match])
    else:
        for value in params.values():
            if type(value) == dict:
                check = check_layer(value, match)
                if check[0] is True:
                    return check
        return (False, None)