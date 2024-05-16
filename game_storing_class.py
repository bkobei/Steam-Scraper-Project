class game_storing:
    def __init__(self, name, genre_list, developer, publisher, prices, sale_percent="0%"):
        self.name = name
        self.genres = genre_list
        self.prices = prices
        if type(genre_list) is not list:
            print("arg2 is invalid. Double check inputs.")
            raise TypeError
        
        if type(prices) is not list:
            print("arg2 is invalid type. Double check inputs.")
            raise TypeError

        self.developer = developer
        self.publisher = publisher
        self.sale_percent = sale_percent

    def get_name(self):
        return self.name
    
    def get_genres(self):
        return self.genres
        
    def get_developer(self):
        return self.developer
    
    def get_publisher(self):
        return self.publisher
        
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
        
    def get_sale_percent(self):
        return self.sale_percent
        
    def is_discounted(self):
        if len(self.prices > 1):
            return True
        else:
            return False
        
class game_storing_2:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def get_position(self):
        return self.position
        
    def get_name(self):
        return self.name
    
    
    