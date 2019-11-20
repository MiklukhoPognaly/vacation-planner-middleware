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
            if not self.data['show_to_affiliates'].lower() == "true":
                return False
            return True

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
            if not self.data['actual'].lower() == 'true':
                return False
            return True

    def get_data(self):
        chunk = []
        for item in self.raw_data['data']:
            chunk.append(BasePricesLatest.InternalDataObject(item))
        return chunk

    def get_success(self):
        if not self.raw_data['success']:
            return False
        return True

