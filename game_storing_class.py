class game_storing:
    def __init__(self, name, genre_list, developer, publisher):
        self.name = name
        self.genres = genre_list
        if type(genre_list) is not list:
            print("arg2 is invalid. Double check inputs.")
            raise TypeError

        self.developer = developer
        self.publisher = publisher

    def get_name(self):
        return self.name
    
    def get_genres(self):
        return self.genres
        
    def get_developer(self):
        return self.developer
    
    def get_publisher(self):
        return self.publisher
        
    def is_discounted(self):
        if self.prices[1] < self.prices[0]:
            return True
        else:
            return False
        
class game_storing_2:
    def __init__(self, name, prices, position):
        self.name = name
        self.prices = prices
        self.position = position

        if type(prices) is not list:
            print("arg2 is invalid type. Double check inputs.")
            raise TypeError
    def get_position(self):
        return self.position
        
    def get_name(self):
        return self.name
    
    def get_prices(self):
        return self.prices
    
    def get_original_price(self):
        return self.prices[0]
    
    def get_discount_price(self):
        if self.is_discounted():
            return self.prices[1]
        else:
            print("There is no discount")
            return self.get_original_price()