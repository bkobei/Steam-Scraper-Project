"""
Created on Wednesday May 13, 2024
@author: Alvin Yu
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
    

download_dir =  'D:/CS4540/Project' #'C:/TestingWithoutDDrive/'      
save_path = os.path.normpath(os.path.join(download_dir, 'Data'))

analyze_data(save_path)