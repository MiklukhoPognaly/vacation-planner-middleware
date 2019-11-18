import requests
#todo:использовать асинхронный вызов http


def get_json_raw(url, *querystring):
    _r = requests.get(url, *querystring)
    return _r.json()


def get_json(url):
    return requests\
        .get(url)\
        .json()
