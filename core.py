import requests
import datefinder
import unittest

def get_json_raw(url, *querystring):
    _r = requests.get(url, *querystring)
    return _r.json()


def mapping(url, *querystring):
    _r = get_json_raw(url, *querystring)
    if 'prices' in _r.keys():
        return _r['prices']
    return _r['errors']


params = {
    'currency': 'usd',
    'period_type': 'year',
    'year': '30',
    'depart_month': '2020-03-01'
}

#1593.0
#{'return_date': '2020-03-02', 'price': 20718.0, 'depart_date': '2020-02-18'}

#1789.0
#{'return_date': '2020-04-06', 'price': 23261.0, 'depart_date': '2020-03-24'}

#1942.0
#{'return_date': '2020-04-17', 'price': 23312.0, 'depart_date': '2020-04-05'}

def get_delta_in_days(itemdict, key):
    for i in datefinder.find_dates(itemdict[key]):
       return i


def calculus(json, _min, _max):
    for item in json:
        _delta = (get_delta_in_days(item, 'return_date') - get_delta_in_days(item, 'depart_date')).days
        if _min < _delta < _max:
            price = item['price']
            try:
               print(price//_delta)
            except Exception:
               price
            else:
                print(item)

class BaseCityClass(object):
    def __init__(self, city_IATA_dict):
        self._city_IATA_dict = city_IATA_dict

    def get_name(self):
        return self._city_IATA_dict['name']

    def get_tzone(self):
        return self._city_IATA_dict['time_zone']

    def get_IATA(self):
        return self._city_IATA_dict['code']

    def get_coordinates(self):
        return self._city_IATA_dict['coordinates']

    def get_name_translations(self):
        return self._city_IATA_dict['name_translations']

    def get_cases(self):
        return self._city_IATA_dict['cases']

    def get_country_code(self):
        return self._city_IATA_dict['country_code']

class BaseSupportedDirections(object):

    class __InternalOrigin(object):
        def __init__(self, data):
            self._raw_data = data

        def get_iata(self):
            return self._raw_data['iata']

        def get_name(self):
            return self._raw_data['name']

        def get_country(self):
            return self._raw_data['country']

        def get_coordinates(self):
            return self._raw_data['coordinates']

    class __InternalDirections(object):
        def __init__(self, data):
            self._raw_data = data

        def get_direct(self):
            return self._raw_data['direct']

        def get_iata(self):
            return self._raw_data['iata']

        def get_name(self):
            return self._raw_data['name']

        def get_country(self):
            return self._raw_data['country']

        def get_coordinates(self):
            return self._raw_data['coordinates']

    def __init__(self, data_supported_directions):
        self._raw_data = data_supported_directions

    def get_origin(self):
        _origin_raw_data = self._raw_data['origin']
        return BaseSupportedDirections.__InternalOrigin(_origin_raw_data)

    def get_directions(self):
        _chunk = []
        for item in self._raw_data['directions']:
            _chunk.append(BaseSupportedDirections.__InternalDirections(item))
        return _chunk




def get_IATA_list(url):
    return requests\
        .get(url)\
        .json()

def IATA_list_parser(IATA_json):
    for city_params_dict in IATA_json:
        city = BaseCityClass(city_params_dict)
        print(city.get_name(), city.get_IATA(), city.get_tzone(), city.get_coordinates())

if __name__ == "__main__":
    IATA_list_parser(get_IATA_list())