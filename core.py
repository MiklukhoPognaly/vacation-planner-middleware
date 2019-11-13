import requests
import datefinder

def get_json_raw(url, *querystring):
    _r = requests.get(url, *querystring)
    return _r.json()


def mapping(url, *querystring):
    _r = get_json_raw(url, *querystring)
    if 'prices' in _r.keys():
        return _r['prices']
    return _r['errors']


params = {
    'affiliate': 'false',
    'origin_iata': 'MOW',
    'destination_iata': 'ROM',
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


if __name__ == "__main__":
    print(calculus(mapping('https://lyssa.aviasales.ru/date_picker_prices', params), 4, 14))
