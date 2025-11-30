"""
Module handles restaurants browsing functionalities
"""
# Unit tests for RestaurantBrowsing class
import unittest
from restaurant_db_stub import StubRestaurantDB

class RestaurantBrowsing:
    """
    A class for browsing restaurants in a database based on
    various criteria like cuisine type, location, and rating.
    
    Attributes:
        database (RestaurantDatabase): An instance of RestaurantDatabase that holds restaurant data.
    """

    def __init__(self, database):
        """
        Initialize RestaurantBrowsing with a reference to a restaurant database.
        
        Args:
            database (RestaurantDatabase): The database object containing restaurant information.
        """
        self.database = database

    def valid_database(self):
        """ validate that database has required keys with proper values """

        required = {"name", "cuisine", "location", "rating"}

        for restaurant in self.database.get_restaurants():
            # Has to have all keys
            if not required.issubset(restaurant.keys()):
                return False

            # Rating cannot be neg number
            rating = restaurant.get("rating")
            if not isinstance(rating, (int, float)) or rating < 0:
                return False

        return True

    def search_by_cuisine(self, cuisine_type):
        """
        Search for restaurants based on their cuisine type.
        
        Args:
            cuisine_type (str): The type of cuisine to filter by (e.g., "Italian").
        
        Returns:
            list: A list of restaurants that match the given cuisine type.

        upd. Validates whether db data is correct
        """
        if not self.valid_database():
            return {"Status": "db failure", "description": "invalid restaurant data"}

        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['cuisine'].lower() == cuisine_type.lower()]

    def search_by_location(self, location):
        """
        Search for restaurants based on their location.
        
        Args:
            location (str): The location to filter by (e.g., "Downtown").
        
        Returns:
            list: A list of restaurants that are located in the specified area.

        upd. Validates whether db data is correct
        """
        if not self.valid_database():
            return {"Status": "db failure", "description": "invalid restaurant data"}

        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['location'].lower() == location.lower()]

    def search_by_rating(self, min_rating):
        """
        Search for restaurants based on their minimum rating.
        
        Args:
            min_rating (float): The minimum acceptable rating to filter by (e.g., 4.0).
        
        Returns:
            list: A list of restaurants that have a rating greater than
            or equal to the specified rating.

        upd. Validates whether db data is correct
        """
        if not self.valid_database():
            return {"Status": "db failure", "description": "invalid restaurant data"}

        return [restaurant for restaurant in self.database.get_restaurants()
                if restaurant['rating'] >= min_rating]

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        """
        Search for restaurants based on multiple filters: cuisine type, location, and/or rating.
        
        Args:
            cuisine_type (str, optional): The type of cuisine to filter by.
            location (str, optional): The location to filter by.
            min_rating (float, optional): The minimum acceptable rating to filter by.
        
        Returns:
            list: A list of restaurants that match all specified filters.
        
        upd. Validates whether db data is correct
        """
        if not self.valid_database():
            return {"Status": "db failure", "description": "invalid restaurant data"}

        results = self.database.get_restaurants() # init to prevent unbound error

        if cuisine_type:
            results = [restaurant for restaurant in results
                       if restaurant['cuisine'].lower() == cuisine_type.lower()]

        if location:
            results = [restaurant for restaurant in results
                       if restaurant['location'].lower() == location.lower()]

        if min_rating:
            results = [restaurant for restaurant in results
                       if restaurant['rating'] >= min_rating]

        return results


class RestaurantDatabase: # pylint: disable=too-few-public-methods
    """
    A simulated in-memory database that stores restaurant information.
    
    Attributes:
        restaurants (list): 
            A list of dictionaries, where each dictionary represents a restaurant with
            fields like name, cuisine, location, rating, price range, and delivery status.
    """

    def __init__(self):
        """
        Initialize the RestaurantDatabase with a predefined set of restaurant data.
        """
        self.restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5,
             "price_range": "$$", "delivery": True},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8,
             "price_range": "$$$", "delivery": False},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0,
             "price_range": "$", "delivery": True},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2,
             "price_range": "$", "delivery": True},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9,
             "price_range": "$$", "delivery": True}
        ]

    def get_restaurants(self):
        """
        Retrieve the list of restaurants in the database.
        
        Returns:
            list: A list of dictionaries, where each dictionary contains restaurant information.
        """
        return self.restaurants


class TestRestaurantBrowsing(unittest.TestCase):
    """
    Unit tests for the RestaurantBrowsing class, testing various search functionalities.
    """

    def setUp(self):
        """
        Set up the test case by initializing a RestaurantDatabase and RestaurantBrowsing instance.

        upd. correct and incorrect db for db query tests
        """
        self.database = [
            ("correct", RestaurantDatabase()),
            ("incorrect", StubRestaurantDB())
        ]

        # self.database = RestaurantDatabase()
        # self.browsing = RestaurantBrowsing(self.database)

    def run_with_both_dbs(self, test_function):
        """ 
        Helper function to run tests with correct and incorrect dbs
        """
        for db_label, db in self.database:
            with self.subTest(db=db_label):
                browsing = RestaurantBrowsing(db)
                test_function(browsing, db_label)

    def test_search_by_cuisine(self):
        """
        Test searching for restaurants by cuisine type.

        upd. if else for testing correct and incorrect db
        """
        def test_both(browsing, db_label):
            results = browsing.search_by_cuisine("Italian")

            if db_label == "correct":
                self.assertEqual(len(results), 2)  # There should be 2 Italian restaurants
                self.assertTrue(
                all(
                    restaurant['cuisine'] == "Italian" for restaurant in results
                    )
                )  # Check if all returned restaurants are Italian
            else:
                self.assertEqual(results["Status"], "db failure") # db data is wrong

        self.run_with_both_dbs(test_both)

    def test_search_by_location(self):
        """
        Test searching for restaurants by location.

        upd. if else for testing correct and incorrect db
        """
        def test_both(browsing, db_label):
            results = browsing.search_by_location("Downtown")

            if db_label == "correct":
                self.assertEqual(len(results), 2)  # There should be 2 restaurants located Downtown
                self.assertTrue(
                    all(
                       restaurant['location'] == "Downtown" for restaurant in results
                    )
                    )  # Check if all returned restaurants are in Downtown
            else:
                self.assertEqual(results["Status"], "db failure") # db data is wrong

        self.run_with_both_dbs(test_both)

    def test_search_by_rating(self):
        """
        Test searching for restaurants by minimum rating.
        
        upd. if else for testing correct and incorrect db
        """
        def test_both(browsing, db_label):
            results = browsing.search_by_rating(4.0)

            if db_label == "correct":
                self.assertEqual(len(results), 4)  # should be 4 restaurants with a rating >= 4.0
                self.assertTrue(
                    all(
                        restaurant['rating'] >= 4.0 for restaurant in results
                    )
                )  # Check if all returned restaurants have a rating >= 4.0
            else:
                self.assertEqual(results["Status"], "db failure") # db data is wrong

        self.run_with_both_dbs(test_both)

    def test_search_by_filters(self):
        """
        Test searching for restaurants by multiple filters
        (cuisine type, location, and minimum rating).
        
        upd. if else for testing correct and incorrect db
        """
        def test_both(browsing, db_label):
            results = browsing.search_by_filters(
                cuisine_type="Italian",
                location="Downtown",
                min_rating=4.0
                )

            if db_label == "correct":
                self.assertEqual(len(results), 1)  # Only one restaurant should match
                self.assertEqual(
                results[0]['name'],
                "Italian Bistro"
            )  # The result should be "Italian Bistro"
            else:
                self.assertEqual(results["Status"], "db failure") # db data is wrong

        self.run_with_both_dbs(test_both)

if __name__ == '__main__':
    unittest.main()
