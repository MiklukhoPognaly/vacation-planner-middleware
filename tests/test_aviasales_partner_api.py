import unittest
from datetime import datetime
from api_facade.aviasales_partner_api import BasePricesLatest, BasePricesCheap


class TestBaseAviasalesPricesLatest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data_aviasales_prices_latest = {
                                                    "success": "true",
                                                    "data": [
                                                        {
                                                            "show_to_affiliates": True,
                                                            "origin": "WMI",
                                                            "destination": "WRO",
                                                            "depart_date": "2015-12-07",
                                                            "return_date": "2015-12-13",
                                                            "number_of_changes": "0",
                                                            "value": "1183",
                                                            "found_at": "2015-09-22T14:08:45+04:00",
                                                            "distance": "298",
                                                            "actual": True
                                                        }
                                                    ]
                                                }

    def test_success(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).success == True

    def test_data_show_to_affiliates(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].show_to_affiliates == True

    def test_data_origin(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].origin == "WMI"

    def test_data_destination(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].destination == "WRO"

    def test_data_depart_date(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].depart_date == datetime.strptime('2015-12-07', "%Y-%m-%d")

    def test_data_return_date(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].return_date == datetime.strptime('2015-12-13', "%Y-%m-%d")

    def test_data_number_of_changes(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].number_of_changes == 0

    def test_data_value(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].value == 1183

    def test_data_found_at(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].distance == 298

    def test_data_actual(self):
        self.assertTrue(BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].actual)


class TestBasePricesCheap(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data_aviasales_prices_cheap = {
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

    def test_success(self):
        self.assertTrue(BasePricesCheap(self.test_data_aviasales_prices_cheap).success)

    def test_data_HKT_first(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap).get_data()[0].show_to_affiliates == True

    def test_data_origin(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].origin == "WMI"

    def test_data_destination(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].destination == "WRO"

    def test_data_depart_date(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].depart_date == datetime.strptime('2015-12-07', "%Y-%m-%d")

    def test_data_return_date(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].return_date == datetime.strptime('2015-12-13', "%Y-%m-%d")

    def test_data_number_of_changes(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].number_of_changes == 0

    def test_data_value(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].value == 1183

    def test_data_found_at(self):
        assert BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].distance == 298

    def test_data_actual(self):
        self.assertTrue(BasePricesLatest(self.test_data_aviasales_prices_latest).get_data()[0].actual)