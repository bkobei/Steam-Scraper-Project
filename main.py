"""
Created on Wednesday April 24, 2024
@author: Brandon Kobayashi
"""


import os
from steam_scraper import SteamScraper
from data_clean import *




# Let's test out the code
download_dir =  "<Your prefered directory for storing data>"       
save_path = os.path.normpath(os.path.join(download_dir, 'Data'))

# Parameters
# For our purposes, latest date will be the week of 4/16 to 4/23
week = "2024-04-16"              # Input as YYYY-MM-DD or YYYY/MM/DD
number_of_weeks = 1          # Input number of weeks of game data you want to collect
max_number_of_games = 500        # Test with max number of games

steam_scraper = SteamScraper(save_path, number_of_weeks, max_number_of_games, week)
steam_scraper.collect_game_data()
steam_scraper.collect_weekly_top_seller()
steam_scraper.driver_quit()
steam_scraper.save_data_to_json()
clean_data(save_path)
analyze_clean_data(save_path)

del steam_scraper
