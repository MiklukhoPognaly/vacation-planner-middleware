import utils.decorators
import utils.http_requests


class BasePricesLatest(object):
    def __init__(self, raw_data, token=None):
        self.raw_data = raw_data
        self.token = token
        self.success = self.get_success()

    class InternalDataObject(object):
        def __init__(self, data):
            self.data = data
            self.show_to_affiliates = self.get_show_to_affiliates()
            self.origin = self.get_origin()
            self.destination = self.get_destination()
            self.depart_date = self.get_depart_date()
            self.return_date = self.get_return_date()
            self.number_of_changes = self.get_number_of_changes()
            self.value = self.get_value()
            self.distance = self.get_distance()
            self.actual = self.get_actual()

        def get_show_to_affiliates(self):
            return self.data['show_to_affiliates']

        def get_origin(self):
            return self.data['origin']

        def get_destination(self):
            return self.data['destination']

        @utils.decorators.datetime_formatter_method_decorator()
        def get_depart_date(self):
            return self.data['depart_date']

        @utils.decorators.datetime_formatter_method_decorator()
        def get_return_date(self):
            return self.data['return_date']

        def get_number_of_changes(self):
            return int(self.data['number_of_changes'])

        def get_value(self):
            return int(self.data['value'])

        def get_distance(self):
            return int(self.data['distance'])

        def get_actual(self):
           return self.data['actual']

    def get_data(self):
        chunk = []
        for item in self.raw_data['data']:
            chunk.append(BasePricesLatest.InternalDataObject(item))
        return chunk

    def get_success(self):
        if not self.raw_data['success']:
            return False
        return True


class BasePricesCheap(object):
    def __init__(self, raw_data, city_iata):
        self.data = raw_data
        self.city_iata = city_iata
        self.success = self.get_success()

    class InternalClassObject(object):
        def __init__(self, data):
            self.data = data
            self.price = self.get_price()
            self.airline = self.get_airline()
            self.flight_number = self.get_flight_number()
            self.departure_at = self.get_departure_at()
            self.return_at = self.get_return_at()
            self.expires_at = self.get_expires_at()

        def get_price(self):
            return self.data['price']

        def get_airline(self):
            return self.data['airline']

        def get_flight_number(self):
            return self.data['flight_number']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def get_departure_at(self):
            return self.data['departure_at']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def get_return_at(self):
            return self.data['return_at']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def get_expires_at(self):
            return self.data['expires_at']

    def get_data(self):
        chunk = []
        for _, raw_data in self.data['data'][self.city_iata].items():
            chunk.append(BasePricesCheap.InternalClassObject(raw_data))
        return chunk

    def get_success(self):
        return self.data['success']


# http://api.travelpayouts.com/v2/prices/month-matrix?
# currency=rub
# &origin=LED
# &destination=HKT
# &show_to_affiliates=true
# &token=РазместитеЗдесьВашТокен

class BasePricesMonthMatrix(object):
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.data_list = self.__get_data()
        self.success = self.__get_success()

    class InternalClassObject(object):
        def __init__(self, data):
            self.data = data
            self.show_to_affiliates = self.__get_show_to_affiliates()
            self.trip_class = self.__get_trip_class()
            self.origin = self.__get_origin()
            self.destination = self.__get_destination()
            self.depart_date = self.__get_depart_date()
            self.return_date = self.__get_return_date()
            self.number_of_changes = self.__get_number_of_changes()
            self.value = self.__get_value()
            self.distance = self.__get_distance()

        def __get_show_to_affiliates(self):
            return self.data['show_to_affiliates']

        def __get_trip_class(self):
            return self.data['trip_class']

        def __get_origin(self):
            return self.data['origin']

        def __get_destination(self):
            return self.data['destination']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%d')
        def __get_depart_date(self):
            return self.data['depart_date']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%d')
        def __get_return_date(self):
            return self.data['return_date']

        def __get_number_of_changes(self):
            return self.data['number_of_changes']

        def __get_value(self):
            return self.data['value']

        def __get_distance(self):
            return self.data['distance']


    def __get_data(self):
        chunk = []
        for object in self.__raw_data['data']:
            chunk.append(BasePricesMonthMatrix.InternalClassObject(object))
        return chunk

    def __get_success(self):
        return self.__raw_data['success']

class BasePricesDirect(object):
    def __init__(self, data, destination):
        self.destination = destination
        self.__raw_data = data
        self.success = self.__get_success()
        self.data_list = self.__get_data()

    def __get_success(self):
        return self.__raw_data['success']

    def __get_data(self):
        chunk = []
        for _, object in self.__raw_data['data'][self.destination].items():
            chunk.append(BasePricesDirect.InternalObject(object))
        return chunk

    class InternalObject(object):
        def __init__(self, data):
            self.__raw_data = data
            self.price = self.__get_price()
            self.airline  = self.__get_airline()
            self.flight_number = self.__get_flight_number()
            self.departure_at = self.__get_departure_at()
            self.return_at = self.__get_return_at()
            self.expires_at = self.__get_expires_at()

        def __get_price(self):
            return self.__raw_data['price']

        def __get_airline(self):
            return self.__raw_data['airline']

        def __get_flight_number(self):
            return self.__raw_data['flight_number']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def __get_departure_at(self):
            return self.__raw_data['departure_at']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def __get_return_at(self):
            return self.__raw_data['return_at']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def __get_expires_at(self):
            return self.__raw_data['expires_at']


class BasePricesCalendar(object):
    def __init__(self, data):
        self.data = data
        self.success = self.get_success()
        self.data_list = self.get_data()

    def get_success(self):
        return self.data['success']

    def get_data(self):
        chunk = []
        for _, dictionary in self.data['data'].items():
            chunk.append(BasePricesCalendar.InternalClassObject(dictionary))
        return chunk

    class InternalClassObject(object):
        def __init__(self, data):
            self.data = data
            self.origin = self.__get_origin()
            self.destination = self.__get_destination()
            self.price = self.__get_price()
            self.transfers = self.__get_transfers()
            self.airline = self.__get_airline()
            self.flight_number = self.__get_flight_number()
            self.departure_at = self.__get_departure_at()
            self.return_at = self.__get_return_at()
            self.expires_at = self.__get_expires_at()

        def __get_origin(self):
            return self.data['origin']

        def __get_destination(self):
            return self.data['destination']

        def __get_price(self):
            return self.data['price']

        def __get_transfers(self):
            return self.data['transfers']

        def __get_airline(self):
            return self.data['airline']

        def __get_flight_number(self):
            return self.data['flight_number']

        @utils.decorators.datetime_formatter_method_decorator("%Y-%m-%dT%H:%M:%SZ")
        def __get_departure_at(self):
            return self.data['departure_at']

        @utils.decorators.datetime_formatter_method_decorator("%Y-%m-%dT%H:%M:%SZ")
        def __get_return_at(self):
            return self.data['return_at']

        @utils.decorators.datetime_formatter_method_decorator("%Y-%m-%dT%H:%M:%SZ")
        def __get_expires_at(self):
            return self.data['expires_at']


class BasePricesNearestPlacesMatrix(object):
    def __init__(self, data):
        self.data = data
        self.prices_list = self.__prices_list()

    def __prices_list(self):
        chunk = []
        for item in self.data['prices']:
            chunk.append(BasePricesNearestPlacesMatrix.InternalClassObject(item))
        return chunk

    class InternalClassObject(object):
        def __init__(self, data):
            self.data = data
            self.value = self.__get_value()
            self.trip_class = self.__get_trip_class()
            self.show_to_affiliates = self.__get_show_to_affiliates()
            self.return_date = self.__get_return_date()
            self.origin = self.__get_origin()
            self.number_of_changes = self.__get_number_of_changes()
            self.gate = self.__get_gate()
            self.found_at = self.__get_found_at()
            self.duration = self.__get_duration()
            self.distance = self.__get_distance()
            self.destination = self.__get_destination()
            self.depart_date = self.__get_depart_date()
            self.actual = self.__get_actual()

        def __get_value(self):
            return self.data['value']

        def __get_trip_class(self):
            return self.data['trip_class']

        def __get_show_to_affiliates(self):
            return self.data['show_to_affiliates']

        @utils.decorators.datetime_formatter_method_decorator()
        def __get_return_date(self):
            return self.data['return_date']

        def __get_origin(self):
            return self.data['origin']

        def __get_number_of_changes(self):
            return self.data['number_of_changes']

        def __get_gate(self):
            return self.data['gate']

        @utils.decorators.datetime_formatter_method_decorator('%Y-%m-%dT%H:%M:%SZ')
        def __get_found_at(self):
            return self.data['found_at']

        def __get_duration(self):
            return self.data['duration']

        def __get_distance(self):
            return self.data['distance']

        def __get_destination(self):
            return self.data['destination']

        @utils.decorators.datetime_formatter_method_decorator()
        def __get_depart_date(self):
            return self.data['depart_date']

        def __get_actual(self):
            return self.data['actual']
