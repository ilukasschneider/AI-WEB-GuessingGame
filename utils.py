import json
import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space
import random
import os

# number of allowed guesses
GUESS_COUNT = 6

animals = json.load(open(r'animals.json', 'r'))

# Define the file path for storing game stats
stats_file = 'game_stats.json'

# Function to load or create game stats from a file
def load_game_stats():
    if os.path.exists(stats_file):
        # If the file exists, load it
        with open(stats_file, 'r') as file:
            return json.load(file)
    else:
        # If the file does not exist, create it with default values
        default_stats = {'games': [] }
        with open(stats_file, 'w') as file:
            json.dump(default_stats, file)
        return default_stats  # Return the default values

# Function to save game stats to a file
def save_game_stats(clue_number, is_won, guess_evaluation):
    stats = load_game_stats()  # Load current stats

    stats['games'].append([clue_number, is_won, guess_evaluation])

    # Save updated stats back to the file
    with open(stats_file, 'w') as file:
        json.dump(stats, file)

# delete the current stats file and create a new one filled with default values

def delete_stats():
    os.remove(stats_file)
    load_game_stats()


def get_traits(animal1, animal2):

    trait1, trait2 = None, None
    for animal in animals:
        if animal['name'] == animal1:

            trait1 = {'Class': animal['taxonomy']['class'],
              'Location': animal['locations'],
              'Diet': animal['characteristics']['diet'],
                'Prey': animal['characteristics']['main_prey']
                      }

        if animal['name'] == animal2:

            trait2 = {'Class': animal['taxonomy']['class'],
              'Location': animal['locations'],
              'Diet': animal['characteristics']['diet'],
                'Prey': animal['characteristics']['main_prey']
                }

    return trait1, trait2


def compare_traits(animal1, animal2):
    traits1, traits2 = get_traits(animal1, animal2)

    shared = {}
    if traits1 and traits2:
        for trait in ['Class', 'Diet', 'Prey']:
            if traits1[trait] == traits2[trait]:
                shared[trait] = traits1[trait]

        # Compare 'location' as a special case
    locations1 = set(traits1['Location'])
    locations2 = set(traits2['Location'])
    common_locations = locations1.intersection(locations2)

    # Add shared locations to shared traits
    if common_locations:
        shared['Location'] = ", ".join(common_locations)

    return shared


def uncover_card(shared_traits):
    if shared_traits:
        num = len(shared_traits)
        topCols_count = min(num, 2)
        buttonCols_count = max(0, num-topCols_count)

        topCols = st.columns(topCols_count)


        for k in range(topCols_count):
            with topCols[k]:
                key = list(shared_traits.keys())[k]
                ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        if buttonCols_count > 0:
            buttonCols = st.columns(buttonCols_count)
            for k in range(buttonCols_count):
                with buttonCols[k]:
                    key = list(shared_traits.keys())[k+topCols_count]
                    ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        space()
    else:
        st.title("Unfortunately no commonalities")
