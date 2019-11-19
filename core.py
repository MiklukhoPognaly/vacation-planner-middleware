import datefinder

from api_facade.data_cities import BaseCityClass
from utils.http_requests import get_json_raw, get_json
import utils.http_requests
import api_facade.min_prices_aviasales

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

#todo:использовать асинхронный вызов http




def form_best_prices():

    _cities_iata = utils.http_requests.get_json('http://api.travelpayouts.com/data/ru/cities.json')

    _cities_iata_1 = api_facade.data_cities.BaseCityClass(_cities_iata).get_iata()[4]
    _cities_iata_2 = api_facade.data_cities.BaseCityClass(_cities_iata).get_iata()[56]



    _raw_json = utils.http_requests.get_json_raw(
        'http://min-prices.aviasales.ru/calendar_preload',
                {
                    "origin": "MOW",
                    "destination": _cities_iata_2.get_IATA(),
                    "depart_date": "2019-12-01",
                    "one_way": "true"
                }
    )

    inst = api_facade.min_prices_aviasales.BaseCalendarPreload(_raw_json)

    for price in inst.get_best_prices():
        print(price.get_origin, price.get_distance, price.get_depart_date(), price.get_return_date(), price.get_value())


if __name__ == "__main__":
    form_best_prices()