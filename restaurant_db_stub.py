""" Stub incorrect restaurant database """

class StubRestaurantDB:
    """ Restaurant database with incorrect data """

    def __init__(self):
        """ Stub db having wrong parameters and negative rating """

        self.restaurants = [
            {"what": "Italian Bistro", "is": "Italian", "this": "Downtown", "rating": 4.5,
             "price_range": "$$", "delivery": True}, # wrong keys
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": -1.6,
             "price_range": "$$$", "delivery": False}, # negative rating
            {"cuisine": "Mexican", "location": "Downtown",
             "price_range": "$", "delivery": True} # missing keys
        ]

    def get_restaurants(self):
        return self.restaurants
