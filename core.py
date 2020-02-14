from WeatherFacadeApi import weatherApi as wh
from OtherFacadeApi import citiesIataList as cl
from AviasalesFacadeApi import aviasales_min_prices

if __name__ == "__main__":
    response_json = cl.request_cities_iata_list()
    town = cl.BaseCitiesClass(response_json).get_iata()[-1].name_translations['en']



