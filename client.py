from logic import tickets
from services.elasticsearch import eservice
import os
import config

def client_job():
    director = tickets.Director()
    builder = tickets.ConcreteBuilder1()
    director.builder = builder
    director.build_file_to_upload()
    Upload = eservice.PerformUpload(
        elastic_url=config.elastic_url,
        mapping=config.elastic_data_mapping)
    Upload.perform_upload(filename_path=os.path.join(config.UPLOAD_FILE, 'MOW_weather_tickets.json')
                            , doc_type=config.doc_type
                            , index_name=config.elastic_index_name)


if __name__ == "__main__":
    client_job()

