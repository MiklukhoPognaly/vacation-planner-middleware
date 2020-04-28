from logic import tickets
from unittest import TestCase
from mapping import maptickets
import credentials

cheap_test_data = {
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



class TestProduct1(TestCase):
    def setUp(self):
        self.Product1 = tickets.Product1()
        self.db_data = [{'arrival_iata': 'TEST1'}, {'arrival_iata': 'TEST2'}]
        self.test_data = maptickets.BasePricesCheap(raw_data=cheap_test_data, city_iata='HKT').object_list

    def test_form_db_list_with_routes(self):
        self.Product1.form_db_list_with_routes(tst_res=self.db_data)
        self.assertEqual(self.Product1.routes, [{'arrival_iata': 'TEST1'}, {'arrival_iata': 'TEST2'}])


    def test_form_list_with_cheap_ticket_flights(self):
        self.Product1.routes = [{"arrival_iata": "ROM"}]
        self.Product1.form_list_with_cheap_ticket_flights('MOW')
        self.assertIn('price', self.Product1.flights[0])


class TestUniversalGetMethod(TestCase):
    def setUp(self):
        self.destination = 'ROM'
        self.mapping = maptickets.BasePricesCheap

    def test_false_get_info(self):
        _ = maptickets.get_info_from_api_with_mapping(self.destination
                                           , api='http://api.travelpayouts.com/v1/prices/cheap'
                                           , mapping=self.mapping
                                           , url_params={'currency': 'RUB',
                                                         'origin': 'MOW',
                                                         'destination': self.destination,
                                                         'token': credentials.TRAVELPAYOUTS_TOKEN
                                                         })
        self.assertIn('price', _[0].data.keys())
