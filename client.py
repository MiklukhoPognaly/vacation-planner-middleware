from logic import tickets
from services.elasticsearch import eservice
import os
import pathlib

if __name__ == "__main__":
    # file creation
    director = tickets.Director()
    builder = tickets.ConcreteBuilder1()
    director.builder = builder
    director.build_file_to_upload()
    # indexing files in elasticsearch
    mapping = {
        "properties": {
            "airline": {"type": "text"},
            "arrival_iata": {"type": "text"},
            "country": {"type": "text"},
            "departure_at": {"type": "date"},
            "expires_at": {"type": "date"},
            "feelslike": {"type": "long"},
            "flight_number": {"type": "long"},
            "lat": {"type": "text"},
            "lon": {"type": "text"},
            "name": {"type": "text"},
            "price": {"type": "long"},
            "return_at": {"type": "date"},
            "temperature": {"type": "long"}
        }
    }
    filepath = pathlib.Path.home() / 'PyCharmProjects' / 'vacation-planner' / 'vacation_planner' / 'files' / 'Moscow' / 'MOW_weather_tickets.json'

    Upload = eservice.PerformUpload(
        elastic_url='https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com',
        mapping=mapping)
    Upload\
        .perform_del_index('aviasales')\
        .perform_upload(filename_path=filepath
                        , doc_type="fly_info"
                        , index_name="aviasales")
