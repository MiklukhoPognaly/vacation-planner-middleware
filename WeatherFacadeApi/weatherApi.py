import requests

#todo: добавить обработку ошибок, {'code': 615, 'type': 'request_failed', 'info': 'Your API request failed. Please try again or contact support.'}
class WeatherApiDataFacade(object):
    def __init__(self, data):
        self.__raw_data = data
        if not self.__raw_data['success']:
            raise TypeError('{}'.format(self.__raw_data['error']['info']))
        #self.country = self.__get_country()
        self.temperature = self.__get_temperature()
        self.feelslike = self.__get_feelslike_temparature()

   #def __get_country(self):
        #return self.__raw_data['location']['country']

    def __get_temperature(self):
        return self.__raw_data['current']['temperature']

    def __get_feelslike_temparature(self):
        return self.__raw_data['current']['feelslike']

    def form_json(self):
        return {
            #"country": self.country,
            "temperature": self.temperature,
            "feelslike": self.feelslike
        }


def weather_data(en_city_name, url='http://api.weatherstack.com/current'):
    _required_data = {"access_key": "51f4c2edda095011cdf4c5c124074567", "query": en_city_name, "units": "m"}
    response_json = requests.get(url, params=_required_data).json()
    return WeatherApiDataFacade(response_json)

