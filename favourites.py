"""Favourite cuisine management"""

import unittest

class Favourites:
    """Functionality for managing a single favourite cuisine"""

    def __init__(self):
        self.favourite = None  # Only one favourite

    def add_favourite(self, cuisine):
        """
        set the favourite cuisine
        """
        self.favourite = cuisine

    def remove_favourite(self):
        """
        remove the favourite cuisine
        """
        self.favourite = None

    def get_favourite(self):
        """
        return the current favourite
        """
        return self.favourite


class TestFavourites(unittest.TestCase):
    """Unittests for Favourites"""

    def setUp(self):
        """ sets up test instance """
        self.favs = Favourites()

    def test_add_favourite(self):
        """ adds favourite """
        cuisine = "Japanese"
        self.favs.add_favourite(cuisine)
        self.assertEqual(self.favs.get_favourite(), cuisine)

    def test_remove_favourite(self):
        """ removes favourite """
        cuisine = "Fast Food"
        self.favs.add_favourite(cuisine)
        self.favs.remove_favourite()
        self.assertIsNone(self.favs.get_favourite())

    def test_initially_none(self):
        """ checks that none after init """
        self.assertIsNone(self.favs.get_favourite())


if __name__ == '__main__':
    unittest.main()
