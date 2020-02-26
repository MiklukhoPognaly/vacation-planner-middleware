class BaseJsonPurifier(object):
    """
    The base class for all operations with the formation of JSON objects for subsequent indexing in Elasticsearch.
    """

    def form_json(self, data, path, filename):
        pass

    def get_raw_data(self):
        pass
