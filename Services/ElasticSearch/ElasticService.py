import requests
import json

#curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-Type: application/json' -d
#curl -X POST "localhost:9200/_bulk?pretty" -H 'Content-Type: application/json' -d'

#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, helpers
import os, uuid

# create a new instance of the Elasticsearch client class
elastic = Elasticsearch("https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com")

'''
a simple function that gets the working path of
the Python script and returns it
'''
def script_path():
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': # posix is for macOS or Linux
        path = path + "/"
    else:
        path = path + chr(92) # backslash is for Windows
    return path


'''
this function opens a file and returns its
contents as a list of strings split by linebreaks
'''
def get_data_from_file(self, path=script_path()):
    with open(path + str(self), encoding="utf8", errors='ignore') as wf:
        data = wf.read()
    return json.loads(data)

'''
make a mapping for file
'''
def setup_mapping(index, body, doc_type,):
    elastic.indices.put_mapping(
        index=index,
        doc_type=doc_type,
        body=body,
        include_type_name=True
    )


'''
generator to push bulk data from a JSON
file into an Elasticsearch index
'''
def bulk_json_data(json_file, _index, doc_type):
    json_list = get_data_from_file(json_file)
    for doc in json_list:
    # use a `yield` generator so that the data
    # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }

def delete_all(url=r"https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com/*"):
    _r = requests.delete(url)
    return _r.text


if __name__ == "__main__":

    # airline text
    # arrival_iata text
    # country text
    # departure_at date
    # expires_at date
    # feelslike text
    # flight_number long
    # lat text
    # lon text
    # name text
    # price long
    # return_at date
    # temperature text
    #print(delete_all())
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
    try:
        # make the bulk call, and get a response
        index = "aviasales"
        doc_type = "fly_info"
        response = helpers.bulk(elastic, bulk_json_data("../fly_info_with_weather.json", "aviasales", "fly_info"))
        setup_mapping(index=index, doc_type=doc_type, body=mapping)
        print("\nbulk_json_data() RESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)
