# -*- coding: utf-8 -*-
import requests
import json
from elasticsearch import Elasticsearch, helpers
import os
import uuid
from config import elastic_url as el
# create a new instance of the Elasticsearch client class

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

host = el # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'ap-south-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

elastic = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)






def script_path():
    """
    a simple function that gets the working path of
    the Python script and returns it
    :return: str
    """
    path = os.path.dirname(os.path.realpath(__file__))
    if os.name == 'posix': # posix is for macOS or Linux
        path = path + "/"
    else:
        path = path + chr(92) # backslash is for Windows
    return path


def get_data_from_file(path):
    """
    this function opens a file and returns its
    contents as a list of strings split by linebreaks
    :param self:
    :param path:
    :return: json dict
    """

    with open(path, encoding="utf8", errors='ignore') as wf:
        data = wf.read()
    return json.loads(data)


def setup_mapping(index, body, doc_type,):
    """
    make a mapping for file
    :param index:
    :param body:
    :param doc_type:
    :return:
    """

    elastic.indices.put_mapping(
        index=index,
        doc_type=doc_type,
        body=body,
        include_type_name=True
    )


def bulk_json_data(json_file, _index, doc_type):
    """
    generator to push bulk data from a JSON file into an Elasticsearch index
    :param json_file:
    :param _index:
    :param doc_type:
    :return:
    """
    json_list = get_data_from_file(json_file)
    for doc in json_list:
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }


def delete_all(url=r"https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com/*"):
    """
    delete all indices.
    Warning! Can cause deletion of system indices like .kibana
    :param url:
    :return: str
    """
    _r = requests.delete(url)
    return _r.text


def display_current_mapping(base_url, old_index, changed_mapping):
    """
    get current mapping
    :param base_url:
    :param old_index:
    :param changed_mapping:
    :return: dict
    """
    r = requests.get('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    content = r.json()
    mappings = content[old_index]['mappings']
    mappings['properties'].update(changed_mapping)
    return mappings


def create_index(base_url, new_index, mappings):
    """
    Create a new index with the correct mappings
    :param base_url:
    :param new_index:
    :param mappings:
    :return: None
    """
    r = requests.put('{base_url}/{index_name}'.format(base_url=base_url, index_name=new_index), json={
        'mappings': mappings
    })
    r.raise_for_status()
    return


def perform_reindex(base_url, old_index, new_index):
    """
    function performing reindex
    :param base_url:
    :param old_index:
    :param new_index:
    :return: None
    """
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


def delete_index(base_url, old_index):
    """
    function delete old index
    :param base_url:
    :param old_index:
    :return: None
    """
    r = requests.delete('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    return


def create_alias(base_url, new_index, old_index):
    """
    Create an alias (so that on next time this will be easier to do without downtime)
    :param base_url:
    :param new_index:
    :param old_index:
    :return:
    """
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


class PerformUpload:
    """
    Клиентский класс для загрузки файлов в индекс elasticsearch
    """
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
        if not self._client:
            self._client = Elasticsearch(el)

        if self._client.indices.exists(index=index_name):
            self.perform_del_index(index_name)

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
    Upload = PerformUpload(elastic_url='https://vpc-production-elasticsearch-fuc6vzlsrdejg637pq3557fgei.ap-south-1.es.amazonaws.com', mapping=mapping)
    Upload.elastic_client = elastic
    Upload\
        .perform_del_index('aviasales')\
        .perform_upload(filename_path="../fly_info_with_weather.json", doc_type="fly_info", index_name="aviasales")

