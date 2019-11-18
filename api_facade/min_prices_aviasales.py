from datetime import datetime

class BaseCalendarPreload(object):
    #todo: вынести преобразование формата дат в декоратор.
    def __init__(self, raw_data):
        self._raw_data = raw_data

    class InternalBestPrices(object):
        def __init__(self, raw_data):
            self._raw_data = raw_data

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

        @__value_decorator
        def get_return_date(self):
            return self._raw_data['return_date']

        @__value_decorator
        def get_depart_date(self):
            return datetime.strptime(self._raw_data['depart_date'], "%Y-%m-%d")

        @__value_decorator
        def get_trip_class(self):
            return int(self._raw_data['trip_class'])

        @__value_decorator
        def get_value(self):
            return float(self._raw_data['value'])


    def get_best_prices(self):
        chunk = []
        for item in self._raw_data['best_prices']:
            chunk.append(BaseCalendarPreload.InternalBestPrices(item))
        return chunk
