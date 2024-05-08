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
        data["prices"] = {}
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
                our_json_obj["prices"].update({"normal_price": data["prices"][0]})
                our_json_obj["prices"].update({"discount_price": data["prices"][1]})

                json_objs_list.update({data['name']: our_json_obj})

        amount_of_weeks_recorded += 1

    for (key, item) in json_objs_list.items():
        
        for week in weeks_list:
            if len(item["weekly_positions"]) < 1:
                print("working")
                item["weekly_positions"].update({week: "0"})
        print("weekly_positions amount: %s"%(len(item["weekly_positions"])))
        if len(item["prices"]) < 1:
            item["prices"]["normal_price"] = ""
            item["prices"]["discount_price"] = ""
        print("prices count: %s"%(len(item["prices"])))
        print(item)


    
    
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
