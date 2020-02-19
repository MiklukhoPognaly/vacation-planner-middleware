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


class Airports(Base):
    """ The SQLAlchemy declarative model class for a Airports object. """
    __tablename__ = 'airports'
    id = Column(Integer, primary_key=True)
    airline_iata = Column(Text)
    airline_icao = Column(Text)
    departure_airport_iata = Column(Text)
    departure_airport_icao = Column(Text)
    arrival_airport_iata = Column(Text)
    arrival_airport_icao = Column(Text)
    transfers = Column(Integer)



#Получение данных из сторонних источников
def getDataFromServer(url):
    return [route for route in httpHelpers.getJsonData(url)]

#Загрузка в базу данных
def insertRoutesInDb():
       _r = getDataFromServer(_routes)
       session.bulk_insert_mappings(Routes, _r)
       session.commit()



if __name__ == "__main__":
    insertRoutesInDb()