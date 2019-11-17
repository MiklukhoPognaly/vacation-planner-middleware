# coding=utf-8
import core
import unittest
from api_facade.map_aviasales import BaseSupportedDirections

def test_get_IATA_list():
    result = core.get_IATA_list('http://api.travelpayouts.com/data/ru/cities.json')
    assert isinstance(result, (type([])))

_test_data_IATA_CITIES = {
    'name': 'Тест',
    'time_zone': 'test',
    'code': 'test',
    'cases': {"vi": "", "tv": "", "ro": "", "pr": "", "da": ""},
    'coordinates': {"lon": "000", "lat": "000"},
    'country_code': 'test',
    'name_translations': {"en": "test"},
}

_test_data_supported_directions = {

"origin": {
    "iata": "LED",
    "name": "Санкт-Петербург",
    "country": "RU",
    "coordinates": [30.315785, 59.939039]
    },
"directions":[{
    "direct": 'false',
    "iata": "AAL",
    "name": "Ольборг",
    "country": "DK",
    "coordinates": [9.917771, 57.028811]
    },
    {
    "direct": 'true',
    "iata": "AAQ",
    "name": "Анапа",
    "country": "RU",
    "coordinates": [37.316666, 44.9],
    }]
}


class TestIATABaseClass(unittest.TestCase):
    def setUp(self):
        self._result = core.BaseCityClass(_test_data_IATA_CITIES)

    def test_name(self):
        assert self._result.get_name() == 'Тест'

    def test_tzone(self):
        assert self._result.get_tzone() == 'test'

    def test_IATA(self):
        assert self._result.get_IATA() == 'test'

    def test_coordinates(self):
        assert self._result.get_coordinates() == {"lon": "000", "lat": "000"}

    def test_cases(self):
        assert self._result.get_cases() == {"vi": "", "tv": "", "ro": "", "pr": "", "da": ""}

    def test_name_translations(self):
        assert self._result.get_name_translations() == {"en": "test"}

    def test_country_code(self):
        assert self._result.get_country_code() == 'test'


class TestBaseSupportedDirections(unittest.TestCase):
    def setUp(self):
        self._result = BaseSupportedDirections(_test_data_supported_directions)

    def test_get_origin_iata(self):
        assert self._result.get_origin().get_iata() == "LED"

    def test_get_origin_name(self):
        assert self._result\
                   .get_origin()\
                   .get_name() == "Санкт-Петербург"

    def test_get_origin_country(self):
        assert self._result\
                   .get_origin()\
                   .get_country() == "RU"

    def test_get_origin_coordinates(self):
        assert self._result\
                   .get_origin()\
                   .get_coordinates() == [30.315785, 59.939039]

    def test_directions_direct(self):
        assert self._result\
            .get_directions()[0]\
            .get_direct() == 'false'

    def test_directions_iata(self):
        assert self._result\
            .get_directions()[0]\
            .get_iata() == 'AAL'

    def test_directions_name(self):
        assert self._result\
            .get_directions()[0]\
            .get_name() == 'Ольборг'

    def test_directions_country(self):
        assert self._result\
            .get_directions()[0]\
            .get_country() == 'DK'

    def test_directions_coordinates(self):
        assert self._result\
            .get_directions()[0]\
            .get_coordinates() == [9.917771, 57.028811]
