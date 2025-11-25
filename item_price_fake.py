import unittest
import json
import io

class Price:
    @staticmethod
    def get_price_from_data(data, item_name):
        for item in data["item"]:
            if item["name"] == item_name:
                return item["price"]
        return None

class TestGetPrice(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "item": [
                {"name": "pizza", "price": "9.20"},
                {"name": "hamburger", "price": "7.20"},
                {"name": "salad", "price": "5.20"},
            ]
        }
        # Create fake file object
        self.fake_file = io.StringIO(json.dumps(self.test_data))

    def test_pizza_price(self):
        data = json.load(io.StringIO(json.dumps(self.test_data)))
        self.assertEqual(Price.get_price_from_data(data, "pizza"), "9.20")

    def test_hamburger_price(self):
        data = json.load(io.StringIO(json.dumps(self.test_data)))
        self.assertEqual(Price.get_price_from_data(data, "hamburger"), "7.20")

    def test_salad_price(self):
        data = json.load(io.StringIO(json.dumps(self.test_data)))
        self.assertEqual(Price.get_price_from_data(data, "salad"), "5.20")