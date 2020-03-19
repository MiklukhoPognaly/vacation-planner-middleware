from unittest import TestCase
from utils.helpers import Mdict


class TestMyDict(TestCase):
    def test_add(self):
        _dict1 = {'key1': "value1"}
        _dict2 = {'key2': "value2"}
        self.assertEqual(Mdict(_dict1) + Mdict(_dict2), {'key1': 'value1', 'key2': 'value2'})