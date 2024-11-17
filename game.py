import json
import os
import random
import time
import random
from utils import compare_traits
from utils import uncover_card

# Streamlit-specific imports
import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space

# API-specific imports
from dotenv import load_dotenv
from openai import OpenAI


# ------------- GLOBAL VARIABLES ------------- #


# loads the .env file -> API-KEYS
load_dotenv()
# number of allowed clues
clueCount = 3
# number of allowed guesses
guessCount = 4
# stores the comments for each clue // should be later used to safe GPT-generated answers as cookies so they dont get lost when refreshing the page
clueComments = []
# stores shared traits for each clue // should be saved in cookie variable
sharedTraits = [["water", "wings", "2", "4"],["-", "-", "5", "-"],["flying", "wings", "-", "4"]]
traits = []
# Parsed animal data
animal_data = json.load(open('animals.json', 'r'))
# List of all animal names for the guessing input
animal_names = sorted([animal['name'] for group in animal_data.values() for animal in group])
# solution of the game
winner = animal_names[random.randint(0, len(animal_names) - 1)]
# count how many clues already have been used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
# ------------- HELPER FUNCTIONS ------------- #


# returns a generated comment for a clue via openai-api
def generateClueComment(clueNumber, guess, correctAnswer):
    client = OpenAI(api_key=os.getenv("OPEN-AI-KEY"))
    model = "gpt-4o-mini"
    question = f"The guess was number {clueNumber} and the guess was {guess} and the correct answer was {correctAnswer}. Write a short comment for the user about the guess. Maybe a fun fact about the animal of choice. keep it really short. DO NOT GIVE ANY HINT ABOUT THE CORRECT ANSWERS {correctAnswer} "

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question},
        ],
    )

    return(chat_completion.choices[0].message.content)


# returns a generated comment-stream (!) for a clue via openai-api and also saves the comment inside clueComments array
def streamAndSafeClueComment(clueNumber):
    # appends the GPT-generated comment to the gobal clueComments array
    clueComments.append(generateClueComment(clueNumber, "chicken", "tiger"))
    # this is how this text streming is done in streamlit
    for word in clueComments[clueNumber].split(" "):
        yield word + " "
        # change time of text writing effect
        time.sleep(0.01)


# ------------- RENDERING THE GAME ------------- #


# Streamlit app layout
st.title("Animal Guessing Game")

# dropdown for the user to select an animal name for guessing
user_guess = st.selectbox("What animal do you think this is?", [''] + animal_names)

# the user made a correct guess
if user_guess == winner:
    st.write("Congratulations! You won the game!")
    user_guess = False
#if the selection box has been pressed
if user_guess:
    st.session_state['counter'] += 1
# renders clues based on clueCount and generates a new comment if a comment for a clue is missing/not yet generated yet
    if st.session_state['counter'] <= clueCount:

        i = st.session_state['counter'] - 1

        # get the traits the guessed animal shares with the winner animal
        shared = [compare_traits(winner, user_guess)]
        st.write(shared)
        traits.append(shared)
        with st.container(border=True):
            st.title(f"Clue {st.session_state['counter']}")
            st.header(f"Your guess was: :red[{user_guess}]")
            space()
            space()

            uncover_card(shared, i)
            #topCols = st.columns(2)
            #buttonCols = st.columns(2)
            #with topCols[0]:
                # content for card1
             #   ui.metric_card(title="shared x", content=shared[i], key=f"card{random.randint(0, 20000)}")
            #with topCols[1]:
                # content for card2
             #   ui.metric_card(title="shared x", content=sharedTraits[i][1], key=f"card{random.randint(0, 20000)}")
            #with buttonCols[0]:
                # content for card3
             #   ui.metric_card(title="shared x", content=sharedTraits[i][2], key=f"card{random.randint(0, 20000)}")
            #with buttonCols[1]:
                # content for card4
             #   ui.metric_card(title="shared x", content=sharedTraits[i][3], key=f"card{random.randint(0, 20000)}")
            space()
            space()
            #with st.chat_message("ai"):
             #   if i >= len(clueComments):
              #      st.write_stream(streamAndSafeClueComment(i))
               # else:
                #    st.write(clueComments[i])
            space()
            space()
    if st.session_state['counter'] >= guessCount:
        st.header(f"You lost! The correct animal was {winner}")
