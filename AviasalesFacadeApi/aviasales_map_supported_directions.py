

class BaseSupportedDirections(object):
    """
    TO BE DELETED.\n

    A wrapper class on an external method that returns a list of available
    directions.
    It contains methods:
    `self.iata`,
    `self.name`,
    `self._raw_data`,
    `self.coordinates`
    """
    class __InternalOrigin(object):

        def __init__(self, data):
            self._raw_data = data
            self.iata = self.get_iata()
            self.name = self.get_name()
            self.country = self.get_country()
            self.coordinates = self.get_coordinates()

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
            self.direct = self.get_direct()
            self.iata = self.get_iata()
            self.name = self.get_name()
            self.country = self.get_country()
            self.coordinates = self.get_coordinates()
            self.weather = self.get_weather()
            self.weight = self.get_weight()

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

        def get_weather(self):
            return self._raw_data['weather']

        def get_weight(self):
            return int(self._raw_data['weight'])

    def __init__(self, data_supported_directions):
        self._raw_data = data_supported_directions
        self.origin = self.get_origin()
        self.directions = self.get_directions()

    def get_origin(self):
        _origin_raw_data = self._raw_data['origin']
        return BaseSupportedDirections.__InternalOrigin(_origin_raw_data)

    def get_directions(self):
        _chunk = []
        for item in self._raw_data['directions']:
            _chunk.append(BaseSupportedDirections.__InternalDirections(item))
        return _chunk
