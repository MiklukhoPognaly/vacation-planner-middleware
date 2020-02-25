from vacation_planner import baseClasses
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    Text
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vacation_planner.AviasalesFacadeApi import aviasales_partner_api
from vacation_planner.WeatherFacadeApi import weatherApi


class FormTicketsInfo(baseClasses.BaseJsonPurifier):
    """
    Class for generating information on tickets from the database and weather methods
    """
    def __init__(self, origin_iata):
        self.origin = origin_iata
        self.routes = []
        self.aviasales = []


    def __get_db_routes(self):

        _raw_sql = "Select " \
                   "a.arrival_city_iata" \
                   ",b.name_translations as arrival_city_name " \
                   "from ( " \
                   "Select distinct " \
                   "b.city_code as departure_city_iata " \
                   ",c.city_code as arrival_city_iata " \
                   "from public.routes as a " \
                   "inner join public.iata_mapping as b " \
                   "on a.departure_airport_iata = b.code " \
                   "inner join public.iata_mapping as c " \
                   "on a.arrival_airport_iata = c.code " \
                   "where b.city_code = '{origin}' " \
                   ") a inner join public.cities b " \
                   "on a.arrival_city_iata = b.code " \
                   "inner join public.cities c " \
                   "on a.departure_city_iata = c.code".format(origin=self.origin)


        engine = create_engine(
        'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(user="jurybulich22", password="Citibank09"))

        with engine.connect() as con:
            rs = con.execute(_raw_sql)

            for row in rs:
                self.routes.append({"arrival_iata": row[0], "name": row[1]})
        print('данные из базы получены')
        return self

    def __get_data_from_aviasales(self):
        if self.routes:
            for route in self.routes:
                for item in aviasales_partner_api.get_cheap_prices(self.origin, route['arrival_iata']):
                    item.data.update(route)
                    self.aviasales.append(item.data)
        print('данные от aviasales получены')
        return self

    def get_weather_info(self):
        self.__get_db_routes()
        self.__get_data_from_aviasales()
        for item in self.aviasales[:5]:
            weatherApi.weather_data(item['name'])



    def form_json(self):
        self.__get_db_routes().__get_data_from_aviasales()






if __name__ == "__main__":
    inst = FormTicketsInfo("MOW")
    inst.get_weather_info()
