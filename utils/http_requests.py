import requests
import utils.decorators

#todo:использовать асинхронный вызов http


@utils.decorators.aviasales_api_json_error_decorator
def get_json_raw(url, *querystring):
    _r = requests.get(url, *querystring)
    return _r.json()


def get_json(url):
    return requests\
        .get(url)\
        .json()
