# coding=utf-8
import unittest2
from datetime import datetime

import utils.helpers

def test_get_IATA_list():
    result = utils.helpers.get_json('http://api.travelpayouts.com/data/ru/cities.json')
    assert isinstance(result, (type([])))


_test_data_IATA_CITIES = [{
    'name': 'Тест',
    'time_zone': 'test',
    'code': 'test',
    'cases': {"vi": "", "tv": "", "ro": "", "pr": "", "da": ""},
    'coordinates': {"lon": "000", "lat": "000"},
    'country_code': 'test',
    'name_translations': {"en": "test"},
}]

_test_data_supported_directions = {

    "origin": {
        "iata": "LED",
        "name": "Санкт-Петербург",
        "country": "RU",
        "coordinates": [30.315785, 59.939039]
    },
    "directions":
        [
            {
            "direct": 'true',
            "iata": "AAQ",
            "name": "Анапа",
            "country": "RU",
            "coordinates": [37.316666, 44.9],
            "weight": 0,
            "weather":
                {
                    "weathertype": 'null',
                    "temp_min": 'null',
                    "temp_max": 'null',
                }
            }
        ]
}

test_best_prices_data = {
    "errors": {},
    "current_depart_date_prices": [],
    "best_prices":
        [
            {
                "value": '6787.0',
                "trip_class": '0',
                "show_to_affiliates": 'false',
                "return_date": 'null',
                "origin": "MOW",
                "number_of_changes": '0',
                "gate": "S7",
                "found_at": "2019-11-15T01:52:26",
                "distance": '1209',
                "destination": "AAQ",
                "depart_date": "2020-04-27",
                "actual": 'true'
            },
        ]
}



class TestErrorDecorator(unittest2.TestCase):
    def test_error_http(self):
        with self.assertRaises(Exception):
            utils.http_requests.get_json_raw('http://min-prices.aviasales.ru/calendar_preload',
                                                           {
                                                                "origin": "MOW",
                                                                "destination": "WWW",
                                                                "depart_date": "2019-12-01",
                                                                "one_way": "true"
                                                           })

