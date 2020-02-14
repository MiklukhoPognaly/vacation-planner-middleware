from WeatherFacadeApi import weatherApi as wh
from OtherFacadeApi import citiesIataList as cl


def sum_dictionaries(dict1, dict2):
    dict1.update(dict2)
    return dict1


if __name__ == "__main__":
    response_json = cl.request_cities_iata_list()
    town_object = cl.BaseCitiesClass(response_json).get_iata()[-1]
    weather_object = wh.weather_data(town_object.eng_name)

    print(sum_dictionaries(town_object.form_json(), weather_object.form_json()))
