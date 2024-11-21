import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import altair as alt
from utils import load_game_stats, delete_stats
import numpy as np

from streamlit_js_eval import streamlit_js_eval
#Todo:
# add point system
# handle empty stats
# fix give up button

#binary_data = load_game_stats()
# Sample data for demonstration
# You can replace this with actual data from your game logic
# data = {
#     "Game ID": [1, 2, 3, 4, 5],
#     "Total Guesses": [5, 3, 7, 4, 6],
#     "Good Guesses": [3, 2, 4, 3, 5],
#     "Bad Guesses": [2, 1, 3, 1, 1],
#     "Win": [True, True, False, True, True],
#     "Clues": [3, 4, 2, 5, 1]
# }

values = load_game_stats()['games']
total_games = len(values)
games_won = values.count(True)
games_lost = total_games - games_won
print(total_games, games_won, games_lost, list(range(1, total_games + 1)), values )
data = {
    "Game ID": list(range(1, total_games+1)),
    "Win": values
}
df = pd.DataFrame(data)

# Streamlit app layout
st.title("Guessing Game Statistics")

# Total games played
#total_games = binary_data['games_won'] + binary_data['games_lost']
st.subheader(f"Total Games Played: {total_games}")

# Display overall game statistics
st.write("## Overall Statistics")

# Average number of guesses per game
#avg_guesses = df["Total Guesses"].mean()
# st.write(f"**Average Number of Guesses per Game:** {avg_guesses:.2f}")
#
# # Average number of good guesses per game
# avg_good_guesses = df["Good Guesses"].mean()
# st.write(f"**Average Good Guesses per Game:** {avg_good_guesses:.2f}")
#
# avg_clues = df["Clues"].mean()
# st.write(f"**Average Clues per Game:** {avg_clues:.2f}")

# Win rate
win_rate = df["Win"].mean() * 100
st.write(f"**Win Rate:** {win_rate:.2f}%")

# Summary table for each game
st.write("## Game-by-Game Summary")
st.dataframe(df)

st.session_state.detailed_view = False

# st.write("## Number of Guesses per Game")
# # Use columns to place buttons side by side
# col1, col2 = st.columns(2)
# with col1:
#     if st.button("Show Good and Bad Guesses"):
#         st.session_state.detailed_view = True
# with col2:
#     if st.button("Show Total Guesses"):
#         st.session_state.detailed_view = False
# # Display the appropriate bar chart based on the toggle state
#
# if st.session_state.detailed_view:
#     # Color-coded chart showing Good and Bad Guesses
#     st.bar_chart(df[["Good Guesses", "Bad Guesses"]])
# else:
#     # Default view showing only the Total Guesses
#     st.bar_chart(df[["Total Guesses"]])
#
#
# # Create bar chart using Altair
# chart = alt.Chart(df).mark_bar(color="skyblue").encode(
#     x=alt.X("Game ID:N", title="Game"),
#     y=alt.Y("Clues:Q", title="Number of Clues Used")
# )
#
# # Add the average line
# average_line = alt.Chart(pd.DataFrame({"y": [avg_clues]})).mark_rule(color="red").encode(
#     y='y:Q'
# )
# # Add text label for the average line
# average_text = alt.Chart(pd.DataFrame({"y": [avg_clues]})).mark_text(
#     text=f"Average: {avg_clues:.2f}",  # Beschriftung mit dem Durchschnittswert
#     align='left',  # Linksbündig zur Linie
#     dx=5,  # Kleiner Abstand zur Linie
#     dy=-5,  # Platzierung oberhalb der Linie
#     color="red"
# ).encode(
#     y='y:Q'
# )
#
# # Display the combined chart
# st.write("## Clues Used per Game")
# st.altair_chart(chart + average_line + average_text, use_container_width=True)
#
# st.write("similar barplot for the different levels")


# Display pie chart for win/loss distribution
st.write("## Win/Loss Distribution")
win_loss_count = df["Win"].value_counts()
print(win_loss_count)
st.write("Win-Loss Chart")
st.write("Wins: ", games_won, " Losses: ", games_lost)
# Create a new Figure and Axes
fig, ax = plt.subplots()
win_loss_count.plot.pie(autopct="%1.1f%%", labels=["Win", "Loss"], ax=ax)

ax.set_ylabel('')  # Remove the y-axis label for a cleaner look

# Display the pie chart in Streamlit
st.pyplot(fig)


# reset the stats by deleting the file
if st.button("Reset"):
    delete_stats()
    streamlit_js_eval(js_expressions="parent.window.location.reload()")


# Additional Metrics
# st.write("## Additional Metrics")
# st.write(f"**Maximum Guesses in a Game:** {df['Total Guesses'].max()}")
# st.write(f"**Minimum Guesses in a Game:** {df['Total Guesses'].min()}")
