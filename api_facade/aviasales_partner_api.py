#http://api.travelpayouts.com/v2/prices/latest?
# currency=rub
# &period_type=year
# &page=1
# &limit=30
# &show_to_affiliates=true
# &sorting=price
# &token=РазместитеЗдесьВашТокен
import utils.http_requests

test_data_aviasales_prices_latest = {
    "success": "true",
    "data": [
        {
            "show_to_affiliates": "true",
            "origin": "WMI",
            "destination": "WRO",
            "depart_date": "2015-12-07",
            "return_date": "2015-12-13",
            "number_of_changes": "0",
            "value": "1183",
            "found_at": "2015-09-22T14:08:45+04:00",
            "distance": "298",
            "actual": "true"
        }
    ]
}

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

#http://api.travelpayouts.com/v1/prices/cheap?
# origin=MOW
# &destination=HKT
# &depart_date=2017-11
# &return_date=2017-12
# &token=РазместитеЗдесьВашТокен


data = {
                                   "success": True,
                                   "data": {
                                      "HKT": {
                                         "0": {
                                            "price": 35443,
                                            "airline": "UN",
                                            "flight_number": 571,
                                            "departure_at": "2015-06-09T21:20:00Z",
                                            "return_at": "2015-07-15T12:40:00Z",
                                            "expires_at": "2015-01-08T18:30:40Z"
                                         },
                                         "1": {
                                            "price": 27506,
                                            "airline": "CX",
                                            "flight_number": 204,
                                            "departure_at": "2015-06-05T16:40:00Z",
                                            "return_at": "2015-06-22T12:00:00Z",
                                            "expires_at": "2015-01-08T18:38:45Z"
                                         },
                                         "2": {
                                            "price": 31914,
                                            "airline": "AB",
                                            "flight_number": 8113,
                                            "departure_at": "2015-06-12T13:45:00Z",
                                            "return_at": "2015-06-24T20:30:00Z",
                                            "expires_at": "2015-01-08T15:17:42Z"
                                         }
                                      }
                                   }
        }


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