from requests import get

def request_cities_iata_list(url='http://api.travelpayouts.com/data/ru/cities.json'):
    return get(url).json()



class BaseCitiesClass(object):

    def __init__(self, city_IATA_dict):
        self._city_IATA_dict = city_IATA_dict

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
            self.name_translations = self.__get_name_translations()
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

        def __get_name_translations(self):
            return self._city_IATA_dict['name_translations']

        def __get_cases(self):
            return self._city_IATA_dict['cases']

        def __get_country_code(self):
            return self._city_IATA_dict['country_code']

if __name__ == '__main__':
    response_json = request_cities_iata_list()
    print(BaseCitiesClass(response_json).get_iata()[-1].name)