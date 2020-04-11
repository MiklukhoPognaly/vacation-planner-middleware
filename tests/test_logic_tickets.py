from unittest import TestCase
from logic import tickets


class TestBuilder(TestCase):
    def setUp(self):
        self.test_director = tickets.Director()
        self.test_builder = tickets.ConcreteBuilder1()
        self.test_director.builder = self.test_builder

    def test_builder_part_a(self):
        res = self.test_builder.produce_part_a()
        self.assertGreater(res, 0)

    def test_builder_part_b(self):
        res = self.test_builder.produce_part_b()
        self.assertGreater(res, 0)

    def test_builder_part_c(self):
        res = self.test_builder.produce_part_c()
        self.assertGreater(res, 0)
