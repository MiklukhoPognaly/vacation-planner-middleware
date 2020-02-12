import requests


def getWheatherData(town, url='http://api.weatherstack.com/current'):
    _required_data = {"access_key": "0fd6ea2a8bc39bc0c7583f0dc286a4d0", "query": town, "units": "m"}
    return requests.get(url, params=_required_data).json()