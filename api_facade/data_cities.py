class BaseCityClass(object):

    def __init__(self, city_IATA_dict):
        self._city_IATA_dict = city_IATA_dict

    def get_iata(self):
        chunk = []
        for item in self._city_IATA_dict:
            chunk.append(BaseCityClass.InternalIata(item))
        return chunk

    class InternalIata(object):
        def __init__(self, data):
            self._city_IATA_dict = data

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