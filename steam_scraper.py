"""
Created on Saturday April 20, 2024
@author: Brandon Kobayashi
helpers: Alvin Yu
         Jimmy Nguyen
Edited on April 30, 2024
Edited on May 7, 2024 debugging
"""

import os
import time
import datetime
import json
import math

#from dotenv import load_dotenv
#from decouple import config # type: ignore

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from game_storing_class import game_storing as gs
from game_storing_class import game_storing_2 as gs2

class SteamScraper():
    def __init__(self, save_path, number_of_weeks, max_number_of_games, week=''):
        url = 'https://store.steampowered.com/charts/topsellers/US'
        steam_game_search = 'https://store.steampowered.com/search/'


        self.save_path = save_path
        if not os.path.exists(self.save_path):
            print("[INFO] Save path was not found. Creating a new directory.")
            os.makedirs(self.save_path)

        if not number_of_weeks > 0:
            raise ValueError("Error! You have to input at least 1 number of weeks.\n" + 
                             "TRY AGAIN.")
        
        new_week = ''

        if week != "":
            year = ''
            month = ''
            day = ''
            if '-' in week: 
                try:
                    year, month, day = week.split('-')
                except:
                    raise Exception("If you split with '-', be consistent.")
            elif '/' in week:
                try:
                    year, month, day = week.split('/')
                except:
                    raise Exception("If you split with '/', be consistent.")
            else:
                raise Exception("Invalid Input: Enter proper date after restart")

            try:
                datetime.datetime(int(year), int(month), int(day))
            except:
                raise ValueError("Date is invalid! Try again.")
        
            new_week = year + '-'
            if month[0] == '0':
                month = month[1:]
            
            new_week += month + '-'

            if day[0] == '0':
                day = day[1:]
            
            new_week += day

            print(new_week)
        else:
            print("Week variable is empty, defaulting to latest week")
    
        options = Options()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        if week:
            self.url = url + '/' + new_week
        else:
            self.url = url
        self.url_without_date = url
        self.steam_search_url = steam_game_search
        self.week = new_week
        self.number_of_weeks = number_of_weeks
        self.gamelist = {}
        self.complete_game_list = {}
        self.max_number_of_games = max_number_of_games

    # Self-explanatory: collects the data for games
    def collect_weekly_top_seller(self):
        # Try to find and click the 'show all 100' button
        self.driver.get(self.url)

        weeks_left = self.number_of_weeks
        while weeks_left > 0:
            week_game_list = []
            
            try: 
                WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="page_root"]/div[3]/div/div/div/div[4]/div/button')
                )).click()
                print("Success on clicking 'show all 100' button")
            except: 
                print("Cannot find 'show all 100' button")
                self.driver.quit()

            current_home_url = self.driver.current_url
            week_name = current_home_url.removeprefix(self.url_without_date + '/')
            print("Week name: " + week_name)
                
            time.sleep(5)

            games = self.driver.find_elements(By.CLASS_NAME, '_2-RN6nWOY56sNmcDHu069P')

            game_item_count = 1
            games_stored = 0
            game_max_store = 10

            # for game in games: (for actually scraping)
            # while loop for testing
            for game in games:
                # boolean variables
                is_empty = False
                discount = False
                # lists
                genre_list = []

                # string variables
                game_price = ''
                game_price_discount = ''
                game_name = ''

                # Important xpaths
                game_name_xpath = ("//*[@id=\"page_root\"]/div[3]/div/div/div/div[4]" +
                                "/table/tbody/tr[%s]/td[3]/a/div")

                try: 
                    game_name = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                        (By.XPATH, game_name_xpath%(game_item_count))
                    )).text
                    print("Collecting data for " + game_name)
                except:
                    print("Error Collecting the name of the product. Next product!")
                    continue

                print("===========================================================")
                

                time.sleep(2)
                # Attempt to click on a game
                try:
                    game.click()
                except:
                    print(game_name + " is not clickable")
                    self.driver.quit()

                # Check if current page is age check page
                if 'agecheck' in self.driver.current_url:
                    self.age_check()

                if not (self.is_error_div()):
                    if 'app' in self.driver.current_url:
                        is_game = True
                        # Collect data from game page
                        print("Collecting product data")        
                        
                        is_add_genre_open = False
                        # Try to click on add genre title
                        try: 
                            WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                                (By.XPATH, "//*[@id=\"glanceCtnResponsiveRight\"]/div[2]/div[2]/div")
                            )).click()
                            is_add_genre_open = True
                        except:
                            print("Cannot find add_genre in " + self.driver.current_url)
                            print(game_name + " is likely not a game.")
                            # if cannot find add_genre button, likely not a game
                            is_game = False

                        if is_game:
                            print(game_name + " is a game! Collecting data for " + game_name)

                            # Close add_genre page
                            if is_add_genre_open:
                                self.driver.find_element(By.CLASS_NAME, 'newmodal_close').click()
                            
                            print("Out of while loop")

                            # Check for DLCS or updates of games
                            
                            
                            game_storing_object = gs2(
                                game_name, 
                                games_stored + 1
                                )

                            week_game_list.append(game_storing_object)

                            games_stored += 1

                            print("%s games are now stored"%(games_stored))
                        else:
                            print(game_name + " is not a game.")
                            if is_add_genre_open:
                                self.driver.find_element(By.CLASS_NAME, 'newmodal_close').click()
                    else:
                        print("Not an app webpage.")
                        
                print("Time to go back")
                time.sleep(3)

                # For getting back to home url, would get stuck on game page otherwise

                while self.driver.current_url != current_home_url:
                    self.driver.back()
                    time.sleep(2)
                    
                game_item_count += 1

                print("===========================================================")

            self.gamelist[week_name] = week_game_list

            try:
                WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"page_root\"]/div[3]/div/div/div/div[3]/div[1]/a")
                )).click()
                print("Switched to previous week!")
            except:
                print("Cannot change to previous week.")
                self.driver.quit()
            
            weeks_left -= 1

        print("Time to save data into json files") 

    def collect_game_data(self):
        self.driver.get(self.steam_search_url)

        current_home_url = self.steam_search_url

        game_list = {}

        MAX_ITEM = self.max_number_of_games

        games_stored = 0
        cannot_find_game_title = False
        
        app_id_dict = {}
        app_price_bool_list = []

        # //*[@id="search_resultsRows"]/a[596]
        # //*[@id="search_resultsRows"]/a[293]
        j = 1
        while j <= MAX_ITEM:
            print("============================================")
            print("Collecting App ID No.%s"%j)

            try:
                app_id = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"search_resultsRows\"]/a[%s]"%(j))
                )).get_attribute("data-ds-appid")
                print(app_id)
                key = app_id
                
            except:
                print("Couldn't find it, scrolling down")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
                try:
                    app_id = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"search_resultsRows\"]/a[%s]"%(j))
                    )).get_attribute("data-ds-appid")
                    print(app_id)
                    key = app_id
                except:
                    print("Couldn't get game name. ERROR")

            prices = []
            price_found = False
            is_discount = False

            

            obj = ''


            try:
                app_discount_price = WebDriverWait(self.driver,3).until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"search_resultsRows\"]/a[%s]/div[2]/div[4]/div/div/div[2]/div[2]"%j)   
                )).text
                app_original_price = WebDriverWait(self.driver,2).until(EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id=\"search_resultsRows\"]/a[%s]/div[2]/div[4]/div/div/div[2]/div[1]"%j)
                )).text

                prices.append(app_original_price)
                prices.append(app_discount_price)
                print("Appended Discounted and Original Prices")
                print("Discount Price: %s"%app_discount_price)
                print("Original Price: %s"%app_original_price)
                price_found = True
                is_discount = True
                discount_percent = self.cal_discount_percent(
                        self.price_to_float(prices[0]),
                        self.price_to_float(prices[1])
                    )
                
                discount_percent = str(discount_percent) + '%'
                
                print(discount_percent)

                obj = {
                    "discount_percent": discount_percent,
                    "prices": prices,
                    "is_discount": is_discount,
                    "price_found": price_found
                }
            except:
                print("Couldn't find discount. Checking if normal price.")

                try:
                    app_original_price = WebDriverWait(self.driver,2).until(EC.element_to_be_clickable(
                        (By.XPATH, "//*[@id=\"search_resultsRows\"]/a[%s]/div[2]/div[4]/div/div/div/div"%j)
                    )).text
                    
                    print("Original Price: %s"%app_original_price)
                    prices.append(self.fix_price(app_original_price))
                    price_found = True
                except:
                    print("Couldn't find normal price either.")
                    print("Will get price from store page.")
                    # This is for games where the price is not stored in search page
                obj = {
                    "prices": prices,
                    "is_discount": is_discount,
                    "price_found": price_found
                }

            app_id_dict[key] = obj
            j += 1

            print("============================================")

        print("%s items in app_id_dict"%(len(app_id_dict)))

        for id, obj in app_id_dict.items():
            print("Game/App number %s"%(games_stored+1))
            game_name = ''
            genre_list = []
            original_game_title = ''

            self.driver.get("https://store.steampowered.com/app/%s"%(id))
            
            
            if 'agecheck' in self.driver.current_url:
                self.age_check()

            if not (self.is_error_div()):
                if 'app' in self.driver.current_url:
                    try:
                        original_game_title = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                            (By.XPATH, "//*[@id=\"appHubAppName\"]")
                        )).text
                        game_name = self.fix_name(original_game_title)

                        print("Collecting data for %s"%(original_game_title))
                        print("================================================")
                    except:
                        # cannot_find_game_title = True
                        print("Could not find game title")

                    is_game = True
                    # Collect data from game page
                    print("Collecting product data")        
                    
                    is_add_genre_open = False
                    # Try to click on add genre title
                    try: 
                        WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                            (By.XPATH, "//*[@id=\"glanceCtnResponsiveRight\"]/div[2]/div[2]/div")
                        )).click()
                        is_add_genre_open = True
                    except:
                        print("Cannot find add_genre in " + self.driver.current_url)
                        print(game_name + " is likely not a game.")
                        # if cannot find add_genre button, likely not a game
                        is_game = False

                    if is_game:
                        print(game_name + " is a game! Collecting data for " + game_name)

                        print(game_name + "'s genres: ")

                        j = 1
                        j_max = 4

                        while j <= j_max:
                            time.sleep(2)
                            # Get the genre based on xpath and save in genre_name
                            # //*[@id="app_tagging_modal"]/div/div[2]/div/div[%s]/a
                            genre_href_xpath = "//*[@id=\"app_tagging_modal\"]/div/div[2]/div/div[%s]/a"
                            try:
                                genre_name = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                                    (By.XPATH, genre_href_xpath%(j))
                                )).text
                                print("\t" + genre_name)
                                genre_list.append(genre_name)
                            except:
                                print("Couldn't find " + str(j) + "th genre. Finding next genre!")
                            j += 1

                        # Close add_genre page
                        if is_add_genre_open:
                            self.driver.find_element(By.CLASS_NAME, 'newmodal_close').click()                

                        # Check for DLCS or updates of games

                        # Get developer of game
                        developer_name = ''
                        try:
                            developer_xpath = "//*[@id=\"developers_list\"]/a"
                            developer_name = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                                (By.XPATH, developer_xpath)
                            )).text
                            print("Collected developer")
                        except:
                            print("Cannot find developer for " + game_name + "!")

                        print("Developer: " + developer_name)

                        # Get publisher of game
                        publisher_name = ''
                        try:
                            publisher_xpath = "//*[@id=\"game_highlights\"]/div[1]/div/div[3]/div[4]/div[2]/a"
                            publisher_name = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                                (By.XPATH, publisher_xpath)
                            )).text
                            print("Collected publisher")
                        except:
                            print("Cannot find publisher for " + game_name)

                        print("Publisher: " + publisher_name)
                        
                        if (obj["is_discount"]):
                            game_storing_object = gs(
                                game_name, 
                                genre_list, 
                                developer_name,
                                publisher_name,
                                obj["prices"],
                                obj["discount_percent"])
                        else:
                            game_storing_object = gs(
                                game_name, 
                                genre_list, 
                                developer_name,
                                publisher_name,
                                obj["prices"])

                        game_list[original_game_title] = game_storing_object

                        games_stored += 1
                    else:
                        print(game_name + " is not a game.")
                        if is_add_genre_open:
                            self.driver.find_element(By.CLASS_NAME, 'newmodal_close').click()
                else:
                    print("Not an app webpage.")

                time.sleep(5)

                print("================================================")

        self.complete_game_list = game_list

    # Save collected data in our directory
    def save_data_to_json(self):
        print("Saving game data, please wait...")
        i = 1
        current_save_path = os.path.normpath(os.path.join(self.save_path, 'GameData'))
        if not os.path.exists(current_save_path):
            print("Cannot find 'GameData' folder. Making 'GameData' folder in " + self.save_path)
            os.makedirs(current_save_path)
        else:
            print(current_save_path + " exists in " + self.save_path)

        # Save 5000 games
        for game_name, gs in self.complete_game_list.items():
            print(game_name)
            print(current_save_path)    
            
            game_obj = {
                "position": i,
                "name": gs.get_name(),
                "genre_list": gs.get_genres(),
                "publisher": gs.get_publisher(),
                "developer": gs.get_developer(),
                "prices": gs.get_prices(),
                "discount_percent": gs.get_sale_percent()
            }
            i += 1
            new_game_name = self.fix_name(game_name)
                        
            try:
                filename = "%s.json"%(new_game_name)

                print("Filename: " + filename)

                # Serializing json
                json_object = json.dumps(game_obj, indent=4)

                full_file_path = os.path.normpath(os.path.join(current_save_path, filename))
                print("Filepath: " + full_file_path)

                with open(full_file_path, "w") as outfile:
                    outfile.write(json_object)
                
                print("Success in writing " + filename + " to " + current_save_path)
            except:
                raise Exception("Could not save game obj as json file")
            
        # Save weekly game data
        current_save_path = os.path.normpath(os.path.join(self.save_path, 'Weekly_Tops'))
        for week, list in self.gamelist.items():
            print("Week: " + week)

            current_folder_path = os.path.normpath(os.path.join(current_save_path, week))

            if not os.path.exists(current_folder_path):
                print("Currently making path: " + current_folder_path)
                os.makedirs(current_folder_path)

            for gs in list:

                new_name = self.fix_name(gs.get_name())

                game_obj = {
                    "position": gs.get_position(),
                    "name": new_name,
                }

                try:
                    filename = "%s.json"%(new_name)

                    print("Filename: " + filename)

                    json_object = json.dumps(game_obj, indent=4)

                    full_file_path = os.path.normpath(os.path.join(current_folder_path, filename))
                    print("Filepath: " + full_file_path)

                    with open(full_file_path, "w") as outfile:
                        outfile.write(json_object)

                    print("Success in writing " + filename + " to " + current_folder_path)
                except:
                    raise Exception("Could not save game obj as json file")
                
        print("All files have been saved")
                
    # lowercase the name and rid of abnormal characters      
    def fix_name(self, name):
        new_game_name = ''
        for c in name:
            if ((c >= 'A' and c <= 'Z') or
                (c >= 'a' and c <= 'z') or 
                (c >= '0' and c <= '9')):
                new_game_name += c.lower()
            elif c == ' ':
                new_game_name += '_'

        return new_game_name
    
    def fix_price(self, price):
        fixed_price = ''
        if price == "Free":
            return price
        
        for c in price:
            if ((c >= '0' and c <= '9') or 
                (c == '.') or 
                (c == '$')):
                fixed_price += c
        
        return fixed_price
    
    def cal_discount_percent(self, normal, discount):
        remaining = normal - discount
        return math.floor((remaining/normal)*100)
    
    def price_to_float(self, price):
        float_price = ''
        for c in price:
            if (c >= '0' and c <= '9'):
                float_price += c
        
        return float(float_price)
        

    
    # check if url is age check
    def age_check(self):
        self.driver.find_element(By.ID, 'ageYear').click()
        self.driver.find_element(By.XPATH, '//*[@id="ageYear"]/option[91]').click()
        
        time.sleep(4)

        self.driver.find_element(By.XPATH, '//*[@id="view_product_page_btn"]').click()

    # check for error div in app page
    def is_error_div(self):
        try:
            error = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'error')
            )).text
            print(error)
            return True
        except: 
            print("There is no error div")
            return False

    # Print all data saved in our class
    def print_data(self):
        for week, games in self.gamesList.items():
            print(week)
            for game in games:
                print(game.get_name())
                print(game.get_name() + "'s genres: ")
                for genre in game.get_genres():
                    print("\t" + genre)

                print("Publisher: " + game.get_publisher())
                print("Developer: " + game.get_developer())

    # Collect any data on dlcs
    def collect_dlc_data(self):
        print("Collecting data on any purchasable in store page")

    def driver_quit(self):
        self.driver.quit()

    

            

    
        





