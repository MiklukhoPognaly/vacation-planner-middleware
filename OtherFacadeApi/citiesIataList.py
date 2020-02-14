from requests import get
import unittest
from Helpers import httpHelpers


def request_cities_iata_list(url='http://api.travelpayouts.com/data/ru/cities.json'):
    return get(url).json()



class BaseCitiesClass(object):

    def __init__(self, url="http://api.travelpayouts.com/data/ru/cities.json"):
        self.__request_cities_list(url)
        self.towns = self.get_iata()

    def __request_cities_list(self, url):
        self._city_IATA_dict = httpHelpers.getJsonData(url)

    def get_iata(self):
        chunk = []
        for item in self._city_IATA_dict:
            chunk.append(BaseCitiesClass.InternalIata(item))
        return chunk

    class InternalIata(object):
        def __init__(self, data):
            self._city_IATA_dict = data
            self.name = self.__get_name()
            self.tzone = self.__get_tzone()
            self.iata = self.__get_iata()
            self.coordinates = self.__get_coordinates()
            self.eng_name = self.__get_english_name()
            self.cases = self.__get_cases()
            self.country_code = self.__get_country_code()

        def __get_name(self):
            return self._city_IATA_dict['name']

        def __get_tzone(self):
            return self._city_IATA_dict['time_zone']

        def __get_iata(self):
            return self._city_IATA_dict['code']

        def __get_coordinates(self):
            return self._city_IATA_dict['coordinates']

        def __get_english_name(self):
            return self._city_IATA_dict['name_translations']['en']

        def __get_cases(self):
            return self._city_IATA_dict['cases']

        def __get_country_code(self):
            return self._city_IATA_dict['country_code']

        def form_json(self):
            return {
                'name': self.eng_name,
                'iata': self.iata,
                'coordinates': self.coordinates,
            }

class TestBaseCitiesClass(unittest.TestCase):
    def test_BaseClass(self):
        result = BaseCitiesClass({"sdf":"sdf"})
        self.assertEqual(result.towns, "")


if __name__ == '__main__':
    response_json = request_cities_iata_list()
    print(BaseCitiesClass(response_json).get_iata()[-1].name)