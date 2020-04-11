from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from config import elastic_url as el
from config import doc_type, elastic_index_name

host = el  # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'ap-south-1'  # e.g. us-west-1

service = 'es'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=False,
    connection_class=RequestsHttpConnection
)

print(es.get(index=elastic_index_name, doc_type=doc_type))