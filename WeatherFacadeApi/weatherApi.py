import requests


class WeatherApiDataFacade(object):
    def __init__(self, data):
        self.__raw_data = data
        self.country = self.__get_country()
        self.temperature = self.__get_temperature()
        self.feelslike = self.__get_feelslike_temparature()

    def __get_country(self):
        return self.__raw_data['location']['country']

    def __get_temperature(self):
        return self.__raw_data['current']['temperature']

    def __get_feelslike_temparature(self):
        return self.__raw_data['current']['feelslike']

    def form_json(self):
        return {
            "country": self.country,
            "temperature": self.temperature,
            "feelslike": self.feelslike
        }


def weather_data(en_city_name, url='http://api.weatherstack.com/current'):
    _required_data = {"access_key": "0fd6ea2a8bc39bc0c7583f0dc286a4d0", "query": en_city_name, "units": "m"}
    response_json = requests.get(url, params=_required_data).json()
    return WeatherApiDataFacade(response_json)

