from datetime import datetime
from utils.decorators import datetime_formatter_method_decorator, aviasales_api_json_error_decorator


class BaseCalendarPreload(object):
    #todo: вынести преобразование формата дат в декоратор.
    def __init__(self, raw_data):
        self._raw_data = raw_data

    class InternalBestPrices(object):
        def __init__(self, raw_data):
            self._raw_data = raw_data
            self.distance = self.get_distance()
            self.gate = self.get_gate()
            self.number_of_changes = self.get_number_of_changes()
            self.origin = self.get_origin()
            self.return_date = self.get_return_date()
            self.depart_date = self.get_depart_date()
            self.trip_class = self.get_trip_class()
            self.value = self.get_value()
            self.destination = self.get_destination()

        def __value_decorator(function_to_decorate):
            def wrapper(self):
                if function_to_decorate(self) in ('None', 'none', 'null', 'Null'):
                    return None
                else:
                    return function_to_decorate(self)
            return wrapper

        @__value_decorator
        def get_distance(self):
            return int(self._raw_data['distance'])

        @__value_decorator
        def get_gate(self):
            return self._raw_data['gate']

        @__value_decorator
        def get_number_of_changes(self):
            return int(self._raw_data['number_of_changes'])

        @__value_decorator
        def get_origin(self):
            return self._raw_data['origin']

        @datetime_formatter_method_decorator()
        def get_return_date(self):
            return self._raw_data['return_date']

        @datetime_formatter_method_decorator()
        def get_depart_date(self):
            return self._raw_data['depart_date']

        @__value_decorator
        def get_trip_class(self):
            return int(self._raw_data['trip_class'])

        @__value_decorator
        def get_value(self):
            return float(self._raw_data['value'])

        @__value_decorator
        def get_destination(self):
            return self._raw_data['destination']


    def get_best_prices(self):
        chunk = []
        for item in self._raw_data['best_prices']:
            chunk.append(BaseCalendarPreload.InternalBestPrices(item))
        return chunk
