from Helpers import httpHelpers
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    Text
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

eng = create_engine(
        'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(user="", password=""))

Session = sessionmaker(bind=eng)
session = Session()

#адреса внешних каталогов
_routes = 'http://api.travelpayouts.com/data/routes.json'
_airports = 'http://api.travelpayouts.com/data/ru/airports.json'
_cities = 'http://api.travelpayouts.com/data/cities.json'

#Описание таблиц

Base = declarative_base()

class Routes(Base):
    """ The SQLAlchemy declarative model class for a Route object. """
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    airline_iata = Column(Text)
    airline_icao = Column(Text)
    departure_airport_iata = Column(Text)
    departure_airport_icao = Column(Text)
    arrival_airport_iata = Column(Text)
    arrival_airport_icao = Column(Text)
    transfers = Column(Integer)


class IataMapping(Base):
    """ The SQLAlchemy declarative model class for a Airports object. """
    __tablename__ = 'iata_mapping'
    name = Column(Text)
    flightable = Column(Text)
    code = Column(Text, primary_key=True)
    country_code = Column(Text)
    city_code = Column(Text)


#{"code":"AAA","name":"アナー島","coordinates":{"lon":-145.41667,"lat":-17.05},"time_zone":"Pacific/Tahiti","name_translations":{"en":"Anaa"},"country_code":"PF"}
class Cities(Base):
    """ The SQLAlchemy declarative model class for a Airports object. """
    __tablename__ = 'cities'
    code = Column(Text, primary_key=True)
    name_translations = Column(Text)
    country_code = Column(Text, primary_key=True)
    coordinates_lon = Column(Integer)
    coordinates_lat = Column(Integer)



#Получение данных из сторонних источников
def getDataFromServer(url):
    return [item for item in httpHelpers.getJsonData(url)]


#Формирование csv файла для импорта данных
def formCsvFileWithRoutes(filename):
    with open('./data_for_import/{}.csv'.format(filename), 'w+') as f:
        for route in getDataFromServer(_routes):
            f.write(
                '{},{},{},{},{},{},{}\n'.format(route['airline_iata'],
                                                      route['airline_icao'],
                                                      route['departure_airport_iata'],
                                                      route['departure_airport_icao'],
                                                      route['arrival_airport_iata'],
                                                      route['arrival_airport_icao'],
                                                      route['transfers'])
                    )

def formCsvFileWithIataMapping(filename):
    with open('./data_for_import/{}.csv'.format(filename), 'w+') as f:
        for mapping in getDataFromServer(_airports):
            f.write(
                '{}|{}|{}|{}|{}\n'.format(mapping['name'],
                                                      mapping['flightable'],
                                                      mapping['code'],
                                                      mapping['country_code'],
                                                      mapping['city_code'])
                    )

def formCsvFileWithCities(filename):
    with open('./data_for_import/{}.csv'.format(filename), 'w+', encoding='utf8') as f:
        for city in getDataFromServer(_cities):
            name = city['name_translations']['en']
            code = city['code']
            country = city['country_code']
            try:
                lon = city['coordinates']["lon"]
            except TypeError:
                lon = ""
            try:
                lat = city['coordinates']["lat"]
            except TypeError:
                lat = ""
            f.write('{}|{}|{}|{}|{}\n'.format(code, name, country, lon, lat))



#Загрузка в базу данных
def insertRoutesInDatabase():
    with open('./data_for_import/routes.csv', 'r') as f:
        eng = create_engine(
            'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(
                user="", password="")).raw_connection()
        cursor = eng.cursor()
        cmd = 'COPY routes (airline_iata, airline_icao, departure_airport_iata, departure_airport_icao, arrival_airport_iata, arrival_airport_icao, transfers) FROM STDIN WITH (FORMAT CSV, HEADER FALSE)'
        cursor.copy_expert(cmd, f)
        eng.commit()

def insertIataMappingInDatabase(filename):
    with open('./data_for_import/{}.csv'.format(filename), 'r') as f:
        eng = create_engine(
            'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(
                user="", password="")).raw_connection()
        cursor = eng.cursor()
        cmd = 'COPY iata_mapping (name, flightable, code, country_code, city_code) FROM STDIN WITH (FORMAT CSV, HEADER FALSE, delimiter "|")'
        cursor.copy_expert(cmd, f)
        eng.commit()

def insertCitiesInDatabase(filename):
    with open('./data_for_import/{}.csv'.format(filename), 'r') as f:
        eng = create_engine(
            'postgres://{user}:{password}@vacation-planner-library.ciodtn8hce9y.ap-south-1.rds.amazonaws.com:5432/postgres'.format(
                user="", password="")).raw_connection()
        cursor = eng.cursor()
        cmd = 'COPY cities (code, name_translations, country_code, coordinates_lon, coordinates_lat) FROM STDIN WITH (FORMAT CSV, HEADER FALSE, delimiter "|")'
        cursor.copy_expert(cmd, f)
        eng.commit()

if __name__ == "__main__":
    formCsvFileWithCities('cities')
    insertCitiesInDatabase('cities')