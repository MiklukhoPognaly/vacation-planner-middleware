from unittest import TestCase
from formTicketsJson import FormTicketsInfo
import os

class TestFormTicketsInfo(TestCase):
    def test_form_json(self):
        inst = FormTicketsInfo("TEST", getRoutes=False, getFlyInfo=False, getWeatherData=False)
        inst.form_json(path=".", filename="test.json", data={})

    def tearDown(self):
        os.remove('./test.json')
