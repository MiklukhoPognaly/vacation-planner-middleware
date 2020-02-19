from WeatherFacadeApi import weatherApi as wh
from OtherFacadeApi import citiesIataList as cl
from AviasalesFacadeApi import aviasales_partner_api as mp

def sum_dictionaries(dict1, dict2):
    dict1.update(dict2)
    return dict1




def filterFlightByOrigin(origin):
    #todo: нужно ставить таймауты на вызов mp.get_cheap_prices. Превышаю количество допустимых подключений.
    return [
        mp.get_cheap_prices(iata_town_origin=origin, iata_town_destination=town.iata) for town
        in cl.BaseCitiesClass().towns
        if mp.get_cheap_prices(iata_town_origin=origin, iata_town_destination=town.iata) is not None
    ]





if __name__ == "__main__":

    # town_object = cl.BaseCitiesClass(response_json).towns
    # chunk = []
    # for town in town_object:
    #     a = mp.get_cheap_prices(town.iata)
    #     if a is not None:
    #         chunk.append(town.eng_name)
    # weather_object = wh.weather_data(chunk[5])
    # print(sum_dictionaries(town_object.towns[5].form_json(), weather_object.form_json()))

    print(filterFlightByOrigin('MOW'))
