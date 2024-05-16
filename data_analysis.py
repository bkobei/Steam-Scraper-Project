"""
Created on Monday May 13, 2024
@author: Alvin Yu
Edited Wednesday May 15, 2024
"""

import json
import os

def read_json_files(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                file_data = json.load(file)
                data.append(file_data)

    return data

def overall_genre_count(path):
    genre_count_dict = {}
    for game in path:
        genres = game["genre_list"]
        for genre in genres:
            if genre not in genre_count_dict:
                genre_count_dict[genre] = 1
            else:
                genre_count_dict[genre] += 1
                

    return genre_count_dict

def weekly_genre_count(path):
    weekly_genre_count_dict = {}
    for game in path:
        weeks = game["weekly_positions"]
        genres = game["genre_list"]
        for week in weeks.keys():
            if week not in weekly_genre_count_dict.keys():
                weekly_genre_count_dict[week] = {}
            
            for genre in genres:
                if genre not in weekly_genre_count_dict[week]:
                    weekly_genre_count_dict[week].update({genre: 0})
                
                weekly_genre_count_dict[week][genre] += 1

    return weekly_genre_count_dict

def weekly_prices(path):
    weekly_prices_dict = {}
    for game in path:
        for week in game["weekly_positions"].keys():
            if week not in weekly_prices_dict:
                weekly_prices_dict[week] = {}

    for game in path:
        for week in weekly_prices_dict:
            if week in game["weekly_positions"]:
                if game["discount_percent"] == '0%':
                    weekly_prices_dict[week].update({game["name"]: price_str_to_float(game["normal_price"])})
                else:
                    weekly_prices_dict[week].update({game["name"]: price_str_to_float(game["discount_price"])})
    
    return weekly_prices_dict

def get_week_list(path):
    week_list = []
    for game in path:
        weeks = game["weekly_positions"]
        for week in weeks.keys():
            if week not in week_list:
                week_list.append(week)

    return week_list

def calculate_average_position_by_genre(data):
    genre_positions = {}
    for game in data:    
        genres = game["genre_list"]
        position = game['position']
        for genre in genres:
            if genre in genre_positions:
                genre_positions[genre].append(position)
            else:
                genre_positions[genre] = [position]
        

    average_positions = {}
    for genre, positions in genre_positions.items():
        average_positions[genre] = sum(positions) / len(positions)

    return average_positions

def calculate_average_position_by_price(data):
    total_positions = 0
    total_games = 0
    for game in data:
        total_positions += game['position']
        total_games += 1

    average_position = total_positions / total_games
    return average_position
    

def count_game_by_price(data):
    price_pos_dict = {
        "$0-$10": 0,
        "$10-$20": 0,
        "$20-$30": 0,
        "$30-$40": 0,
        "$40-$50": 0,
        "$60_or_more": 0,
    }
    for game in data:
        game_norm_price = price_str_to_float(game["normal_price"])
        game_disc_price = price_str_to_float(game["discount_price"])
        price_range_str = ''
        if game["discount_percent"] != "0%":
            price_range_str = get_price_range_as_string(game_disc_price)
        else:
            price_range_str = get_price_range_as_string(game_norm_price)

        price_pos_dict[price_range_str] += 1 

    return price_pos_dict

def get_price_range_as_string(game_price):
    price_range_str = ''
    if  game_price < 10:
        price_range_str = "$0-$10"
    elif game_price < 20:
        price_range_str = "$10-$20"
    elif game_price < 30:
        price_range_str = "$20-$30"
    elif game_price < 40:
        price_range_str = "$30-$40"
    elif game_price < 50:
        price_range_str = "$40-$50"
    else:
        price_range_str = "$60_or_more" 

    return price_range_str


def store_highest_position_per_genre(data):
    highest_positions = {}
    for game in data:
        genres = game["genre_list"]
        position = game['position']
        for genre in genres:
            if genre in highest_positions:
                # Since the lower number is higher position, we save lower number as highest position
                if position < highest_positions[genre]:
                    highest_positions[genre] = position
            else:
                highest_positions[genre] = position

    return highest_positions

def price_str_to_float(price):
    new_price = ''
    for c in price:
        if (c >= '0' and c <= '9') or c == '.':
            new_price += c

    return float(new_price)

def analyze_data(path):
    folder_path = os.path.normpath(os.path.join(path, "Clean_Data"))
    games_data = read_json_files(folder_path)

    average_position_by_genre = calculate_average_position_by_genre(games_data)
    
    print("Average position by genre:")
    for genre, avg_position in average_position_by_genre.items():
        print(f"{genre}: {avg_position}")
    
    average_position_by_price = calculate_average_position_by_price(games_data)
    print("\nAverage position by price:", average_position_by_price)

    highest_positions_per_genre = store_highest_position_per_genre(games_data)
    print("\nHighest position per genre:")
    for genre, highest_position in highest_positions_per_genre.items():
        print(f"{genre}: {highest_position}")

    genre_count_dict = overall_genre_count(games_data)
    print("\nOverall Genre Count:")
    for genre, count in genre_count_dict.items():
        print(f"{genre}: {count}")

    week_list = get_week_list(games_data)
    print("\nWeek List")
    for week in week_list:
        print(week)

    print("\nWeekly Genre Count")
    weekly_genres = weekly_genre_count(games_data)
    for week, genre_count_list in weekly_genres.items():
        print("Week of %s"%week)
        print("=================================================")
        for genre, genre_count in reversed(sorted(genre_count_list.items(), key=lambda item: item[1])):
            print("No. of games in %s Genre: "%genre + "%s"%genre_count)

        print("=================================================")

    print("\nWeekly Prices in Top 100")
    weekly_prices_dict = weekly_prices(games_data)
    for week, game_obj in weekly_prices_dict.items():
        print(f"Week of {week}")
        print("==================================================")

        for game, price in game_obj.items():
            print(f"{game}: ${price}")

        print("==================================================")

    print("\nPrice range to count")
    price_range_count_list = count_game_by_price(games_data)
    for range, count in price_range_count_list.items():
        print(f"{range}: {count}")



    json_save_path = os.path.normpath(os.path.join(path, 'Analysis'))
    if not os.path.exists(json_save_path):
        print("Cannot find 'GameData' folder. Making 'GameData' folder in " + path)
        os.makedirs(json_save_path)

    json_obj = {
        "average_positions_by_genre": average_position_by_genre,
        "average_positions_by_price": average_position_by_price,
        "highest_position_per_genre": highest_positions_per_genre,
        "overall_genre_count": genre_count_dict,
        "weekly_genre_count": weekly_genres,
        "weekly_prices": weekly_prices_dict,
        "price_ranges": price_range_count_list
    }

    try:
        filename = "analysis.json"
        json_object = json.dumps(json_obj, indent=4)

        full_file_path = os.path.normpath(os.path.join(json_save_path, filename))
        print("Filepath: " + full_file_path)
        with open(full_file_path, 'w') as outfile:
            outfile.write(json_object)

        print("Success at writing %s"%filename + " to %s"%json_save_path)
    except:
        print("There was an error")

    
