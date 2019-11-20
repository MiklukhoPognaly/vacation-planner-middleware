import requests
from datetime import datetime
#todo:использовать асинхронный вызов http


def aviasales_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        if isinstance(res, dict) and len(res['errors']) > 0:
            raise Exception('Data error occurred: %s ' % res['errors'])
        else:
            return res
    return internal_function


def date_formatter_api_json_error_decorator(function):
    def internal_function(*args, **kwargs):
        res = function(*args, **kwargs)
        try:
            return datetime.strptime(res, "%Y-%m-%d")
        except Exception:
            return datetime.now()

    return internal_function


#@aviasales_api_json_error_decorator

def get_json_raw(url, *querystring):
    _r = requests.get(url, *querystring)
    return _r.json()


def get_json(url):
    return requests\
        .get(url)\
        .json()
