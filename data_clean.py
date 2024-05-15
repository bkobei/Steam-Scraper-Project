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
        item_dir = os.path.normpath(os.path.join(game_data_folder, item))

        with open(item_dir, "r") as json_file:
            data = json.load(json_file)
        
        data["weekly_positions"] = {}
        json_objs_list[data['name']] = data

    amount_of_weeks_recorded = 0
    weeks_list = []
    weekly_tops_folder = os.path.normpath(os.path.join(data_folder, 'Weekly_Tops'))
    for folder in os.listdir(weekly_tops_folder):
        week = folder
        weeks_list.append(week)
        print(week)
        week_folder = os.path.normpath(os.path.join(weekly_tops_folder, week))
        print(week_folder)
        for file in os.listdir(week_folder):
            
            file_dir = os.path.normpath(os.path.join(week_folder, file))

            print(file_dir)
            with open(file_dir, "r") as json_file:
                data = json.load(json_file)

            if data['name'] in json_objs_list:
                our_json_obj = json_objs_list[data['name']]


                our_json_obj["weekly_positions"].update({week: data['position']})

                json_objs_list.update({data['name']: our_json_obj})

        amount_of_weeks_recorded += 1

    for item in json_objs_list.values():
        if "prices" not in item:
            item["prices"] = ["$0", "$0"]

        if len(item["prices"]) < 1:
            item["prices"].append("$0")
            item["prices"].append("$0")
        elif len(item["prices"]) < 2:
            item["prices"].append("$0")

        print("Before price clean: %s"%item)
        if (item["prices"][0] == "Free" or
            item["prices"][0] == "free"):
            item["prices"][0] = "$0"


        item["normal_price"] = item["prices"][0]
        item["discount_price"] = item["prices"][1]

        print("After price clean: %s"%item)




    
    
    clean_data_path = os.path.normpath(os.path.join(data_folder, 'Clean_Data'))
    if not os.path.exists(clean_data_path):
        print("[INFO] Clean data path was not found. Creating a new directory.")
        os.makedirs(clean_data_path)

    for item in json_objs_list.values():
        try:
            filename = "%s_clean.json"%(item["name"])        

            file_path = os.path.normpath(os.path.join(clean_data_path, filename))
        
            clean_json_obj = json.dumps(item, indent=4)

            print("Attempting to save %s"%filename + " to %s"%clean_data_path)

            with open(file_path, "w") as outfile:
                outfile.write(clean_json_obj)

            print("Successful in writing to %s"%clean_data_path)
        except:
            print("Could not save file %s"%(filename))

    print("All data cleaned. Done!") 
    
