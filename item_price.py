"""
    Price handler code
    Returns price for item
"""
import unittest
import json

# pylint: disable=too-few-public-methods

class Price:
    """
    Price handler class
    """
    def __init__(self, file, item_name):
        self.file = file
        self.item_name = item_name

    @staticmethod
    def get_price(file, item_name):
        """
        Gets price for wanted item and returns it
        Args:
            file (any): json -file
            item_name (any): item name in json

        Returns:
            Price from json
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data["item"]:
            if item["name"] == item_name:
                return item["price"]
        return None

class TestGetPrice(unittest.TestCase):
    """
    Unittest for item_price
    """
    def setUp(self):
        self.test_file = "testmenu.json"
        self.test_data = {
            "item": [
                {"name": "pizza", "price": "9.20"},
                {"name": "hamburger", "price": "7.20"},
                {"name": "salad", "price": "5.20"},
            ]
        }
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f)

    def test_pizza_price(self):
        """
        Test get_price with "pizza"
        """
        self.assertEqual(Price.get_price(self.test_file, "pizza"), "9.20")

    def test_hamburger_price(self):
        """
        Test get_price with "hamburger"
        """
        self.assertEqual(Price.get_price(self.test_file, "hamburger"), "7.20")

    def test_salad_price(self):
        """
        Test get_price with "salad"
        """
        self.assertEqual(Price.get_price(self.test_file, "salad"), "5.20")

if __name__ == "__main__":
    unittest.main()
