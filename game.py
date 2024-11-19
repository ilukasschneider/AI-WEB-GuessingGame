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
from streamlit_js_eval import streamlit_js_eval

# API-specific imports
from dotenv import load_dotenv
from openai import OpenAI


# ------------- GLOBAL VARIABLES ------------- #

#Todo:
# improve ending of the game

# loads the .env file -> API-KEYS
load_dotenv()
# number of allowed clues
clueCount = 3
# number of allowed guesses
guessCount = 4
# stores the comments for each clue // should be later used to safe GPT-generated answers as cookies so they dont get lost when refreshing the page
clueComments = []
# stores shared traits for each clue // should be saved in cookie variable
#sharedTraits = [["water", "wings", "2", "4"],["-", "-", "5", "-"],["flying", "wings", "-", "4"]]

# Parsed animal data
animal_data = json.load(open(r'betterAnimalDB\animals.json', 'r'))
# List of all animal names for the guessing input
#animal_names = sorted([animal['name'] for group in animal_data.values() for animal in group])
animal_names = sorted([animal['name'] for animal in animal_data])
# solution of the game
if 'winner' not in st.session_state:
    st.session_state['winner'] = animal_names[random.randint(0, len(animal_names) - 1)]
# count how many clues already have been used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

if 'traits' not in st.session_state:
    st.session_state['traits'] = []

if 'user_guess' not in st.session_state:
    st.session_state['user_guess'] = ''

if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
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
    clueComments.append(generateClueComment(clueNumber, f"{st.session_state['user_guess']}", f"{st.session_state['winner']}"))
    # this is how this text streaming is done in streamlit
    for word in clueComments[clueNumber].split(" "):
        yield word + " "
        # change time of text writing effect
        time.sleep(0.01)




# ------------- RENDERING THE GAME ------------- #


# Streamlit app layout
st.title("Animal Guessing Game")

if 'winner' not in st.session_state:
    st.session_state['winner'] = animal_names[random.randint(0, len(animal_names) - 1)]
# count how many clues already have been used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

if 'traits' not in st.session_state:
    st.session_state['traits'] = []

if 'user_guess' not in st.session_state:
    st.session_state['user_guess'] = ''

if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False

if not st.session_state['game_over']:
    # dropdown for the user to select an animal name for guessing
    st.session_state['user_guess'] = st.selectbox("What animal do you think this is?", [''] + animal_names)


    # if the selection box has been pressed
    if st.session_state['user_guess']:
        # the user made a correct guess
        if st.session_state['user_guess'] == st.session_state['winner']:
            st.write("Congratulations! You won the game!")
            st.session_state['game_over'] = True





    # get the traits the guessed animal shares with the winner animal

        elif st.session_state['user_guess'] :
            st.session_state['counter'] += 1

        # renders clues based on clueCount and generates a new comment if a comment for a clue is missing/not yet generated yet


            if st.session_state['counter'] <= clueCount:
                shared = compare_traits(st.session_state['winner'], st.session_state['user_guess'])
                i = st.session_state['counter'] - 1
                if st.session_state['counter'] == clueCount:
                    st.title("You have one last guess! Use it well")
                #traits.append(shared)
                with st.container(border=True):
                    st.title(f"Clue {st.session_state['counter']}")
                    st.header(f"Your guess was: :red[{st.session_state['user_guess']}]")
                    space()
                    space()
                    st.write("Shared traits are: ")
                    space()

                    uncover_card(shared, 0)

                    space()
                    space()
                    #with st.chat_message("ai"):
                     #   if st.session_state['counter'] >= len(clueComments):
                      #      st.write_stream(streamAndSafeClueComment(i))
                       # else:
                        #    st.write(clueComments[i])
                    space()
                    space()
            if st.session_state['counter'] >= guessCount:
                st.session_state['game_over'] = True
                st.header(f"You lost! The correct animal was {st.session_state['winner']}")

if st.session_state['game_over']:

    st.title("You want to play again? Hit Replay")

if st.button("Replay"):

    st.session_state.clear()

    streamlit_js_eval(js_expressions="parent.window.location.reload()")

