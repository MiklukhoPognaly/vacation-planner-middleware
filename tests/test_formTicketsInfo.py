from unittest import TestCase
from formTicketsJson import FormTicketsInfo
import os


class TestFormTicketsInfo(TestCase):
    def test_form_json(self):
        inst = FormTicketsInfo("TEST", getRoutes=False, getFlyInfo=False, getWeatherData=False)
        inst.form_json(path=".", filename="test.json", data={})

    def tearDown(self):
        os.remove('./test.json')


class TestFormTicketsInfo(TestCase):
    def test_form_json_to_elasticsearch(self):
        inst = FormTicketsInfo("TEST", getWeatherData=False, getRoutes=False, getFlyInfo=False)
        inst.form_json_to_elasticsearch(path='.', filename="test_elasticksearch.json", data=[{"key": "value"}, {"key2": "value2"}])
        with open('./test_elasticksearch.json') as f:
            result = f.readlines()
        self.assertIn('{"key2": "value2"}\n', result)

    def tearDown(self):
        os.remove('./test_elasticksearch.json')
