"""
Created on Wednesday April 24, 2024
@author: Brandon Kobayashi
"""

import json
import os


def clean_data(directory):
    # Check Data Folder
    data_folder = directory
    json_objs_list = {}

    game_data_folder = os.path.normpath(os.path.join(data_folder, 'GameData'))
    game_data_list = []

    for item in os.listdir(game_data_folder):
        with open(item) as json_file:
            data = json.load(json_file)
        
        json_objs_list[data['name']] = data

    weekly_tops_folder = os.path.normpath(os.path.join(data_folder, 'Weekly_Tops'))
    for folder in os.listdir(weekly_tops_folder):
        week = folder
        for file in folder:
            with open(file) as json_file:
                data = json.load(json_file)
            
            if data['name'] in json_objs_list:
                our_json_obj = json_objs_list[data['name']]

                
                

                

                
                    


    
    clean_data_path = os.path.normpath(os.path.join(data_folder, 'Clean_Data'))
    if not os.path.exists(clean_data_path):
            print("[INFO] Clean data path was not found. Creating a new directory.")
            os.makedirs(clean_data_path)

