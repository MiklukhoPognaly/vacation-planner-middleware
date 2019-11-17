

class BaseSupportedDirections(object):

    class __InternalOrigin(object):
        def __init__(self, data):
            self._raw_data = data

        def get_iata(self):
            return self._raw_data['iata']

        def get_name(self):
            return self._raw_data['name']

        def get_country(self):
            return self._raw_data['country']

        def get_coordinates(self):
            return self._raw_data['coordinates']

    class __InternalDirections(object):
        def __init__(self, data):
            self._raw_data = data

        def get_direct(self):
            return self._raw_data['direct']

        def get_iata(self):
            return self._raw_data['iata']

        def get_name(self):
            return self._raw_data['name']

        def get_country(self):
            return self._raw_data['country']

        def get_coordinates(self):
            return self._raw_data['coordinates']

    def __init__(self, data_supported_directions):
        self._raw_data = data_supported_directions

    def get_origin(self):
        _origin_raw_data = self._raw_data['origin']
        return BaseSupportedDirections.__InternalOrigin(_origin_raw_data)

    def get_directions(self):
        _chunk = []
        for item in self._raw_data['directions']:
            _chunk.append(BaseSupportedDirections.__InternalDirections(item))
        return _chunk