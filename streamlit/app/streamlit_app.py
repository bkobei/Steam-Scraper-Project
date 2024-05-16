import streamlit as st
import json
import pandas as pd
# import matplotlib.pyplot as plt

# Load data from the JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load data from JSON file
data = load_data('analysis.json')  # Update with your file path

# Extract genres and counts
# weeks = list(data["weekly_genre_count"].keys())

# Title of the app
st.title('Steam Game Data Analysis')


st.header("Game Genre Counts")
# Dataframe for overall_genre_count 
df_genre = pd.DataFrame.from_dict(data["overall_genre_count"], orient='index', columns=['Counts'])

# Bar graph using Streamlit's built-in functions
st.subheader('Overall Genre Count')
# Display bar graph for the overall genre count
st.bar_chart(df_genre)

# df_genre.plot(kind='pie')

# Week selection dropdown
selected_week = st.selectbox('Select Week', list(data["weekly_genre_count"].keys()))

# Filter data based on selected week
selected_week_genre_data = data['weekly_genre_count'][selected_week]

df_weekly_genre = pd.DataFrame.from_dict(selected_week_genre_data, orient="index", columns=["Counts"])

# Convert filtered data to DataFrame
df_filtered = pd.DataFrame.from_dict(selected_week_genre_data, orient='index', columns=['Counts'])

# Bar graph using Streamlit's built-in functions
st.subheader(f'Game Genres for The Week of {selected_week}')
st.bar_chart(df_filtered)

# Filter data based on selected week
selected_week_price_data = data["weekly_prices"][selected_week]
df_weekly_prices = pd.DataFrame.from_dict(selected_week_price_data, orient="index", columns=["Counts"])

# Convert filtered data to DataFrame
df_filtered2 = pd.DataFrame.from_dict(selected_week_price_data, orient='index', columns=['Counts'])

# Bar graph using Streamlit's built-in functions
st.subheader(f'Game Prices for The Week of {selected_week}')
st.bar_chart(df_filtered2)

# Genre selection
selected_genre = st.selectbox('Select Genre', ['All'] + list(data['weekly_genre_count'][selected_week].keys()))

# Filter data based on selected week and genre

if selected_genre == 'All':
    selected_data = data['weekly_genre_count']
else:
    selected_data = {week: {selected_genre: counts.get(selected_genre, 0)} for week, counts in data['weekly_genre_count'].items()}

# Convert filtered data to DataFrame
df_filtered3 = pd.DataFrame.from_dict(selected_data, orient='index')

# Line graph using Streamlit's built-in functions
st.subheader('Trends of Game Genres Over Weeks')
st.line_chart(df_filtered3)

# Dataframe for price_ranges
df_prices = pd.DataFrame.from_dict(data["price_ranges"], orient='index', columns=["Number of Games in Price"])

# Title of the app
st.header('Price Range Count')

# Bar graph using Streamlit's built-in functions
st.subheader('Price Range Table')
# Display bar graph for the price ranges
st.bar_chart(df_prices)