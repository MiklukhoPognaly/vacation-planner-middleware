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

        @utils.http_requests.date_formatter_api_json_error_decorator
        def get_depart_date(self):
            return self.data['depart_date']

        @utils.http_requests.date_formatter_api_json_error_decorator
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

        def get_departure_at(self):
            return self.data['departure_at']

        def get_return_at(self):
            return self.data['return_at']

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



data = {
   "success": True,
   "data": [
       {
          "show_to_affiliates": True,
          "trip_class": 0,
          "origin": "LED",
          "destination": "HKT",
          "depart_date": "2015-10-01",
          "return_date": "",
          "number_of_changes": 1,
          "value": 29127,
          "found_at": "2015-09-24T00:06:12+04:00",
          "distance": 8015,
          "actual": True
       }
   ]
}

class BasePricesMonthMatrix(object):
    def __init__(self, raw_data):
        self.__raw_data = raw_data
        self.data_list = self.__get_data()
        self.success = self.__get_success()

    class InternalClassObject(object):
        def __init__(self, data):
            self.data = data
            self.show_to_affiliates = self.get_show_to_affiliates()
            self.trip_class = self.get_trip_class()
            self.origin = self.get_origin()
            self.destination = self.get_destination()
            self.depart_date = self.get_depart_date()
            self.return_date = self.get_return_date()
            self.number_of_changes = self.get_number_of_changes()
            self.value = self.get_value()
            self.distance = self.get_distance()

        def get_show_to_affiliates(self):
            return self.data['show_to_affiliates']

        def get_trip_class(self):
            return self.data['trip_class']

        def get_origin(self):
            return self.data['origin']

        def get_destination(self):
            return self.data['destination']

        @utils.http_requests.date_formatter_api_json_error_decorator
        def get_depart_date(self):
            return self.data['depart_date']

        @utils.http_requests.date_formatter_api_json_error_decorator
        def get_return_date(self):
            return self.data['return_date']

        def get_number_of_changes(self):
            return self.data['number_of_changes']

        def get_value(self):
            return self.data['value']

        def get_distance(self):
            return self.data['distance']


    def __get_data(self):
        chunk = []
        for object in self.__raw_data['data']:
            chunk.append(BasePricesMonthMatrix.InternalClassObject(object))
        return chunk

    def __get_success(self):
        return self.__raw_data['success']