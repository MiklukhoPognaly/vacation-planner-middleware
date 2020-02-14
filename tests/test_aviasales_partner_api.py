import unittest2 as unittest
from datetime import datetime
from AviasalesFacadeApi.aviasales_partner_api import BasePricesLatest, BasePricesCheap\
    , BasePricesMonthMatrix, BasePricesDirect, BasePricesCalendar, BasePricesNearestPlacesMatrix


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
        self.assertTrue(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').success)

    def test_data_HKT_first_price(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[0].price == 35443

    def test_data_HKT_second_price(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[1].price == 27506

    def test_data_HKT_first_airline(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[0].airline == "UN"

    def test_data_HKT_second_airline(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[1].airline == "CX"

    def test_data_HKT_first_flight_number(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[0].flight_number, 571)

    def test_data_HKT_second_flight_number(self):
        assert BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT').get_data()[1].flight_number == 204

    def test_data_HKT_first_departure_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[0].departure_at,
                         datetime.strptime("2015-06-09T21:20:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_data_HKT_second_departure_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[1].departure_at,
                         datetime.strptime("2015-06-05T16:40:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_data_HKT_first_return_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[0].return_at,
                         datetime.strptime("2015-07-15T12:40:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_data_HKT_second_return_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[1].return_at,
                         datetime.strptime("2015-06-22T12:00:00Z", '%Y-%m-%dT%H:%M:%SZ'))

    def test_data_HKT_first_expires_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[0].expires_at,
                         datetime.strptime("2015-01-08T18:30:40Z", '%Y-%m-%dT%H:%M:%SZ'))

    def test_data_HKT_second_expires_at(self):
        self.assertEqual(BasePricesCheap(self.test_data_aviasales_prices_cheap, 'HKT')
                         .get_data()[1].expires_at,
                         datetime.strptime("2015-01-08T18:38:45Z", '%Y-%m-%dT%H:%M:%SZ'))


class TestBasePricesMonthMatrix(unittest.TestCase):
    def setUp(self):
        self.test_data = {
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
        self.test_object = BasePricesMonthMatrix(self.test_data)

    def test_success(self):
        self.assertTrue(self.test_object.success)

    def test_data_show_to_affiliates(self):
        self.assertTrue(self.test_object.data_list[0].show_to_affiliates)

    def test_data_trip_class(self):
        self.assertEqual(self.test_object.data_list[0].trip_class, 0)

    def test_data_origin(self):
        self.assertEqual(self.test_object.data_list[0].origin, "LED")

    def test_data_destination(self):
        self.assertEqual(self.test_object.data_list[0].destination, "HKT")

    def test_data_depart_date(self):
        self.assertEqual(self.test_object.data_list[0].depart_date, datetime.strptime('2015-10-01', "%Y-%m-%d"))

    def test_data_return_date(self):
        self.assertEqual(self.test_object.data_list[0].return_date, datetime.now())

    def test_data_number_of_changes(self):
        self.assertEqual(self.test_object.data_list[0].number_of_changes, 1)

    def test_data_value(self):
        self.assertEqual(self.test_object.data_list[0].value, 29127)

    def test_data_distance(self):
        self.assertEqual(self.test_object.data_list[0].distance, 8015)


class TestBasePricesDirect(unittest.TestCase):
    def setUp(self):

        self._raw_data = {
       "success":True,
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
       }}


    def test_get_success(self):
        self.assertTrue(BasePricesDirect(self._raw_data, 'HKT').success)

    def test_get_data_price(self):
            self.assertEqual(BasePricesDirect(self._raw_data, 'HKT').data_list[-1].price, 31914)

    def test_get_data_airline(self):
        self.assertEqual(BasePricesDirect(self._raw_data, 'HKT').data_list[-1].airline, "AB")

    def test_get_data_flight_number(self):
        self.assertEqual(BasePricesDirect(self._raw_data, 'HKT').data_list[-1].flight_number, 8113)

    def htest_get_data_departure_at(self):
        self.assertEqual(BasePricesDirect(self._raw_data, 'HKT')
                         .data_list[-1].departure_at,
                         datetime.strptime("2015-06-12T13:45:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_get_data_return_at(self):
        self.assertEqual(BasePricesDirect(self._raw_data, 'HKT')
                         .data_list[-1].return_at,
                         datetime.strptime("2015-06-24T20:30:00Z", "%Y-%m-%dT%H:%M:%SZ"))

    def test_get_data_expires_at(self):
        self.assertEqual(BasePricesDirect(self._raw_data, 'HKT')
                         .data_list[-1].expires_at,
                         datetime.strptime("2015-01-08T15:17:42Z", "%Y-%m-%dT%H:%M:%SZ"))


class TestBasePricesCalendar(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
           "success": True,
           "data": {
              "2015-06-01": {
                 "origin": "MOW",
                 "destination": "BCN",
                 "price": 12449,
                 "transfers": 1,
                 "airline": "PS",
                 "flight_number": 576,
                 "departure_at": "2015-06-01T06:35:00Z",
                 "return_at": "2015-07-01T13:30:00Z",
                 "expires_at": "2015-01-07T12:34:14Z"
              },
              "2015-06-02": {
                 "origin": "MOW",
                 "destination": "BCN",
                 "price": 13025,
                 "transfers": 1,
                 "airline": "PS",
                 "flight_number": 578,
                 "departure_at": "2015-06-02T17:00:00Z",
                 "return_at": "2015-06-11T13:30:00Z",
                 "expires_at": "2015-01-06T17:15:47Z"
              },

              "2015-06-30": {
                 "origin": "MOW",
                 "destination": "BCN",
                 "price": 13025,
                 "transfers": 1,
                 "airline": "PS",
                 "flight_number": 578,
                 "departure_at": "2015-06-30T17:00:00Z",
                 "return_at": "2015-07-23T13:30:00Z",
                 "expires_at": "2015-01-07T20:15:34Z"
              }
           }
        }

        self.result = BasePricesCalendar(self.data)

    def test_success(self):
        self.assertTrue(self.result.success)

    def test_data_origin(self):
        self.assertEqual(self.result.data_list[-1].origin, 'MOW')

    def test_data_destination(self):
        self.assertEqual(self.result.data_list[-1].destination, 'BCN')

    def test_data_price(self):
        self.assertEqual(self.result.data_list[-1].price, 13025)

    def test_data_transfers(self):
        self.assertEqual(self.result.data_list[-1].transfers, 1)

    def test_data_airline(self):
        self.assertEqual(self.result.data_list[-1].airline, "PS")

    def test_data_departure_date(self):
        self.assertEqual(self.result.data_list[-1].departure_at,
                         datetime.strptime("2015-06-30T17:00:00Z", '%Y-%m-%dT%H:%M:%SZ'))

    def test_data_return_at(self):
        self.assertEqual(self.result.data_list[-1].return_at,
                         datetime.strptime("2015-07-23T13:30:00Z", '%Y-%m-%dT%H:%M:%SZ'))

    def test_data_expires_at(self):
        self.assertEqual(self.result.data_list[-1].expires_at,
                         datetime.strptime("2015-01-07T20:15:34Z", '%Y-%m-%dT%H:%M:%SZ'))

    def test_data_flight_number(self):
        self.assertEqual(self.result.data_list[-1].flight_number, 578)


class TestBasePricesNearestPlacesMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
            "prices": [
                {
                    "value": 26000,
                    "trip_class": 0,
                    "show_to_affiliates": True,
                    "return_date": "2018-09-18",
                    "origin": "BAX",
                    "number_of_changes": 0,
                    "gate": "AMADEUS",
                    "found_at": "2018-07-28T04:57:47Z",
                    "duration": "null",
                    "distance": 3643,
                    "destination": "SIP",
                    "depart_date": "2018-09-09",
                    "actual": True
                }
            ],
            "origins": [
                "BAX"
            ],
            "errors": {
                "amadeus": {}
            },
            "destinations": [
                "SIP"
            ]
        }
        self.result = BasePricesNearestPlacesMatrix(self.data)

    def test_prices_value(self):
        self.assertEqual(self.result.prices_list[0].value, 26000)

    def test_prices_trip_class(self):
        self.assertEqual(self.result.prices_list[0].trip_class, 0)

    def test_prices_show_to_affiliates(self):
        self.assertTrue(self.result.prices_list[0].show_to_affiliates)

    def test_prices_return_date(self):
        self.assertEqual(self.result.prices_list[0].return_date, datetime.strptime('2018-09-18', '%Y-%m-%d'))

    def test_prices_origin(self):
        self.assertEqual(self.result.prices_list[0].origin, 'BAX')

    def test_prices_number_of_changes(self):
        self.assertEqual(self.result.prices_list[0].number_of_changes, 0)

    def test_prices_gate(self):
        self.assertEqual(self.result.prices_list[0].gate, 'AMADEUS')

    def test_prices_found_at(self):
        self.assertEqual(self.result.prices_list[0].found_at,
                         datetime.strptime('2018-07-28T04:57:47Z', '%Y-%m-%dT%H:%M:%SZ'))

    def test_prices_duration(self):
        self.assertEqual(self.result.prices_list[0].duration, 'null')

    def test_prices_distance(self):
        self.assertEqual(self.result.prices_list[0].distance, 3643)

    def test_prices_destination(self):
        self.assertEqual(self.result.prices_list[0].destination, 'SIP')

    def test_prices_depart_date(self):
        self.assertEqual(self.result.prices_list[0].depart_date,
                         datetime.strptime('2018-09-09', '%Y-%m-%d'))

    def test_prices_actual(self):
        self.assertTrue(self.result.prices_list[0].actual)
