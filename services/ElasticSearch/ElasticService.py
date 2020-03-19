import requests
import json


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


# Get current mapping
def display_current_mapping(base_url, old_index, changed_mapping):
    r = requests.get('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    content = r.json()
    mappings = content[old_index]['mappings']
    mappings['properties'].update(changed_mapping)
    return mappings

# ------------------------------------------------
# Create a new index with the correct mappings
def create_index(base_url, new_index, mappings):
    r = requests.put('{base_url}/{index_name}'.format(base_url=base_url, index_name=new_index), json={
        'mappings': mappings
    })
    r.raise_for_status()
    return

# ------------------------------------------------
# Reindex
def perform_reindex(base_url, old_index, new_index):
    r = requests.post('{base_url}/_reindex'.format(base_url=base_url), json={
        "source": {
            "index": old_index
        },
        "dest": {
            "index": new_index
        }
    })
    r.raise_for_status()
    return

# ------------------------------------------------
# Delete the old index
def delete_index(base_url, old_index):
    r = requests.delete('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    return

# ------------------------------------------------
# Create an alias (so that on next time this will be easier to do without downtime)
def create_alias(base_url, new_index, old_index):
    r = requests.post('{base_url}/_aliases'.format(base_url=base_url), json={
        "actions": [
            {"add": {
                "alias": old_index,
                "index": new_index
            }}
        ]
    })
    r.raise_for_status()
    return

class PerformUpload():
    '''
    Клиентский класс для загрузки файлов в индекс ElasticSearch
    '''
    def __init__(self, elastic_url: str, mapping: dict):
        self._mapping = mapping
        self._client = None
        self._base_url_elastic = elastic_url

    @property
    def mapping(self) -> dict:
        return self._mapping

    @mapping.setter
    def mapping(self, new_mapping: dict) -> None:
        self._mapping = new_mapping

    @property
    def elastic_client(self) -> Elasticsearch:
        return self._client

    @elastic_client.setter
    def elastic_client(self, client: Elasticsearch) -> None:
        self._client = client

    def perform_del_index(self, index_name: str):
        delete_index(base_url=self._base_url_elastic, old_index=index_name)
        return self

    def perform_upload(self, filename_path: str, index_name: str, doc_type: str):
        try:
            response = helpers.bulk(self._client, bulk_json_data(filename_path, index_name, doc_type))
            setup_mapping(index=index_name, doc_type=doc_type, body=self.mapping)
            print("\nbulk_json_data() RESPONSE:", response)
        except Exception as e:
            print("\nERROR:", e)
        return self




if __name__ == "__main__":

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
    Upload = PerformUpload(elastic_url='https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com', mapping=mapping)
    Upload.elastic_client = elastic
    Upload\
        .perform_del_index('aviasales')\
        .perform_upload(filename_path="../fly_info_with_weather.json", doc_type="fly_info", index_name="aviasales")

