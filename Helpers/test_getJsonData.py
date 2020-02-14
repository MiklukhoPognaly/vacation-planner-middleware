from unittest import TestCase
from Helpers import httpHelpers


class TestGetJsonData(TestCase):
    def setUp(self):
        self.test_url1 = "https://jsonplaceholder.typicode.com/todos/1"
        self.test_url2 = "http:/sdfsdf"

    def test_positive(self):
        response = httpHelpers.getJsonData(self.test_url1)
        self.assertEqual(response, {'completed': False, 'id': 1, 'title': 'delectus aut autem', 'userId': 1})

    def test_negative(self):
        response = httpHelpers.getJsonData(self.test_url2)
        self.assertEqual(response, None)
