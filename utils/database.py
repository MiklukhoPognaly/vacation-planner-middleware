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


#Получение данных из сторонних источников
def getDataFromServer(url):
    return [item for item in httpHelpers.getJsonData(url)]

#Формирование csv файла для импорта данных
def formCsvFileWithRoutes(route):
    with open('./data_for_import/{}.csv'.format(route), 'w+') as f:
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

def formCsvFileWithIataMapping(route):
    with open('./data_for_import/{}.csv'.format(route), 'w+') as f:
        for mapping in getDataFromServer(_airports):
            f.write(
                '{},{},{},{},{},{},{}\n'.format(mapping['name'],
                                                      mapping['flightable'],
                                                      mapping['code'],
                                                      route['departure_airport_icao'],
                                                      route['arrival_airport_iata'],
                                                      route['arrival_airport_icao'],
                                                      route['transfers'])
                    )



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

if __name__ == "__main__":
    insertRoutesInDatabase()