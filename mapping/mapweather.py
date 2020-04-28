# -*- coding: utf-8 -*-
import requests
import credentials

class WeatherApiDataFacade(object):
    def __init__(self, data):
        self.__raw_data = data
        if 'success' in self.__raw_data:
            print('{}'.format(self.__raw_data['error']['info']))
        self.temperature = self.__get_temperature()
        self.feelslike = self.__get_feelslike_temparature()

    def __get_temperature(self):
        try:
            return self.__raw_data['current']['temperature']
        except KeyError:
            return ""

    def __get_feelslike_temparature(self):
        try:
            return self.__raw_data['current']['feelslike']
        except KeyError:
            return ""

    def __get_lat(self):
        try:
            return self.__raw_data['location']['lat']
        except KeyError:
            return ""

    def __get_lon(self):
        try:
            return self.__raw_data['location']['lon']
        except KeyError:
            return ""

    def __get_country(self):
        try:
            return self.__raw_data['location']['country']
        except KeyError:
            return ""

    def form_json(self):
        return {
            "temperature": self.temperature,
            "feelslike": self.feelslike,
        }


def weather_data(en_city_name, url='http://api.weatherstack.com/current'):
    _required_data = {"access_key": credentials.WEATHERSTACK_TOKEN, "query": en_city_name, "units": "m"}
    response_json = requests.get(url, params=_required_data).json()
    return WeatherApiDataFacade(response_json)

