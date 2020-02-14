from unittest import TestCase
from JsonCreator import addAdditionalData

class TestSum_dictionaries(TestCase):
    def test_sum_dictionaries(self):
        self.assertEqual(addAdditionalData.sum_dictionaries({"1": 1}, {"2": 2}), {"1": 1, "2": 2})
