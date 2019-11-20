import datefinder

from api_facade.data_cities import BaseCityClass
from utils.http_requests import get_json_raw, get_json
import utils.http_requests
import api_facade.aviasales_min_prices

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

    _cities_iata_1 = api_facade.data_cities.BaseCityClass(_cities_iata).get_iata()[56]
    _cities_iata_2 = api_facade.data_cities.BaseCityClass(_cities_iata).get_iata()[56]



    _raw_json = utils.http_requests.get_json_raw(
        'http://min-prices.aviasales.ru/calendar_preload',
                {
                    "origin": _cities_iata_1.iata,
                    "destination": _cities_iata_2.iata,
                    "depart_date": "2019-12-01",
                    "one_way": "false"
                }
    )

    inst = api_facade.aviasales_min_prices.BaseCalendarPreload(_raw_json)

    for best_price in inst.get_best_prices():
        print(_cities_iata_1.name,  _cities_iata_2.name,  best_price.value, best_price.return_date - best_price.depart_date)


if __name__ == "__main__":
    form_best_prices()
