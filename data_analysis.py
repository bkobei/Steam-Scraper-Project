import json
import os

def read_json_files(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                file_data = json.load(file)
                data.extend(file_data)
    return data

def calculate_average_position_by_genre(data):
    genre_positions = {}
    for game in data:
        genre = game['genre']
        position = game['position']
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
        genre = game['genre']
        position = game['position']
        if genre in highest_positions:
            if position > highest_positions[genre]:
                highest_positions[genre] = position
        else:
            highest_positions[genre] = position

    return highest_positions

if __name__ == "__main__":
    folder_path = "C:\Clean_Data"
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