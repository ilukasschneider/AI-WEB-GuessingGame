import json
import os
import random
import streamlit as st
from streamlit_space import space
from utils import compare_traits, uncover_card, load_game_stats, save_game_stats
from dotenv import load_dotenv
from openai import OpenAI

# ------------- GLOBAL VARIABLES ------------- #

load_dotenv()

api_key = "your_api_key_here"  # Insert your OpenAI API key here
client = OpenAI(api_key="api_key")
model = "gpt-4o-mini"
load_game_stats()

guessCount = 6
total_rounds = 5

animal_data = json.load(open('betterAnimalDB/animals.json', 'r'))
animal_names = sorted([animal['name'] for animal in animal_data])

score_mapping = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

# ------------ SESSIONSTATE VARIABLES -------------- #

if 'current_round' not in st.session_state:
    st.session_state['current_round'] = 1
if 'total_score' not in st.session_state:
    st.session_state['total_score'] = 0
if 'winner' not in st.session_state:
    st.session_state['winner'] = random.choice(animal_names)
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'user_guess' not in st.session_state:
    st.session_state['user_guess'] = ''
if 'user_guess_history' not in st.session_state:
    st.session_state['user_guess_history'] = []
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
if 'clue_cards' not in st.session_state:
    st.session_state['clue_cards'] = []
if 'clue_comments' not in st.session_state:
    st.session_state['clue_comments'] = []
if 'won' not in st.session_state:
    st.session_state['won'] = False
if 'initial_clue' not in st.session_state:
    st.session_state['initial_clue'] = None
if 'chat_response' not in st.session_state:
    st.session_state['chat_response'] = ""
if 'question_submitted' not in st.session_state:
    st.session_state['question_submitted'] = False

# ------------- HELPER FUNCTIONS ------------- #

def get_initial_clue(animal_name):
    animal = next((a for a in animal_data if a['name'] == animal_name), None)
    if animal and 'characteristics' in animal:
        characteristic_keys = list(animal['characteristics'].keys())
        if characteristic_keys:
            random_key = random.choice(characteristic_keys)
            return random_key, animal['characteristics'][random_key]
    return None, None

def calculate_score(guesses_used):
    return score_mapping.get(guesses_used, 0)

def prepare_next_round():
    st.session_state['current_round'] += 1
    st.session_state['counter'] = 0
    st.session_state['user_guess_history'] = []
    st.session_state['clue_cards'] = []
    st.session_state['game_over'] = False
    st.session_state['winner'] = random.choice(animal_names)
    st.session_state['initial_clue'] = None
    st.session_state['chat_response'] = ""
    st.session_state['question_submitted'] = False

def handle_user_question(question):
    animal = next((a for a in animal_data if a['name'] == st.session_state['winner']), None)
    if animal:
        characteristic = question.lower().strip("?").replace("how many", "").replace("are they", "").strip()
        characteristics = animal.get('characteristics', {})

        if characteristic in characteristics:
            response = characteristics[characteristic]
        else:
            try:
                question_for_openai = f"What do you know about {animal['name']} in terms of {characteristic}?"
                chat_completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": question_for_openai}],
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Error retrieving data: {e}"

        first_sentence = response.split('.')[0]
        scientific_name = first_sentence[first_sentence.find('('):first_sentence.find(')') + 1]

        response = response.replace(animal['name'], "This animal" + " " + scientific_name)
        response = response.replace(animal['name'].lower(), "this animal")

        st.session_state['chat_response'] = response
    else:
        st.session_state['chat_response'] = "We don't have the data"

# ------------- RENDERING THE GAME ------------- #

st.write(f"(Dev) Correct answer: {st.session_state['winner']}")
st.title("Animal Guessing Game")
st.write(f"Round: {st.session_state['current_round']}/{total_rounds}")

if not st.session_state['initial_clue']:
    st.session_state['initial_clue'] = get_initial_clue(st.session_state['winner'])

if st.session_state['initial_clue'][0]:
    clue_key, clue_value = st.session_state['initial_clue']
    st.subheader(f"Clue 1: {clue_key.replace('_', ' ').capitalize()} - {clue_value}")

if st.session_state['game_over']:
    score = calculate_score(st.session_state['counter'] + 1)

    if st.session_state['user_guess'] == st.session_state['winner']:
        st.write(f"Congratulations! {st.session_state['winner']} is the right answer. You won the game!")
    else:
        st.write(f"Game over! You lost! The answer is: {st.session_state['winner']}")
    
    st.write(f"Your score this round: {score} points")
    
    if not st.session_state.get('score_displayed', False):
        st.session_state['total_score'] += score
        st.session_state['score_displayed'] = True
    
    st.write(f"Total score: {st.session_state['total_score']} points")

    if st.session_state['current_round'] < total_rounds:
        if st.button("Next Round"):
            prepare_next_round()
            st.session_state['score_displayed'] = False
    else:
        st.write("Game Over! Thanks for playing.")
        if st.button("Restart Game"):
            st.session_state.clear()

else:
    selectbox_placeholder = st.empty()

    if st.session_state['counter'] < guessCount:
        guesses_left = guessCount - st.session_state['counter']
        
        if st.session_state['counter'] == guessCount - 1 and not st.session_state['question_submitted']:
            st.info("You have 1 guess left.")
            st.subheader("Last Clue: Ask about the animal")
            user_question = st.text_input("E.g., 'Tell me about penguins'")
            if st.button("Submit Question"):
                handle_user_question(user_question)
                st.write(st.session_state['chat_response'])
                st.session_state['question_submitted'] = True

        if st.session_state['question_submitted'] or st.session_state['counter'] < guessCount - 1:
            st.session_state['user_guess'] = selectbox_placeholder.selectbox(
                "What animal do you think this is?",
                [''] + animal_names
            )

            if st.session_state['user_guess']:
                if st.session_state['user_guess'] == st.session_state['winner']:
                    save_game_stats(True)
                    selectbox_placeholder.empty()
                    st.write(f"Congratulations! {st.session_state['winner']} is the right answer. You won the game!")
                    score = calculate_score(st.session_state['counter'] + 1)
                    st.write(f"Your score this round: {score} points")
                    st.session_state['game_over'] = True
                    st.session_state['won'] = True
                    if st.button("Next Round"):
                        st.session_state['total_score'] += score
                        prepare_next_round()
                        st.session_state['score_displayed'] = False
                else:
                    st.session_state['counter'] += 1

                    if guesses_left > 1:
                        st.info(f"You have {guesses_left} guesses left.")
                    else:
                        selectbox_placeholder.empty()
                        st.session_state['game_over'] = True
                        save_game_stats(False)
                        st.write(f"Game over! You lost! The answer is: {st.session_state['winner']}")
                        st.write(f"Your score this round: 0 points")
                        if st.button("Next Round"):
                            prepare_next_round()
                            st.session_state['score_displayed'] = False

                    shared = compare_traits(st.session_state['winner'], st.session_state['user_guess'])
                    st.session_state['clue_cards'].append(shared)
                    st.session_state['user_guess_history'].append(st.session_state['user_guess'])

                    for clue in reversed(range(st.session_state['counter'])):
                        with st.container():
                            st.title(f"Clue {clue + 2}")
                            st.header(f"Your guess was: :red[{st.session_state['user_guess_history'][clue]}]")
                            space()
                            st.write("Shared traits are: ")
                            space()
                            uncover_card(st.session_state['clue_cards'][clue])
                            space()

if st.sidebar.button("Give up current quiz and count as loss"):
    save_game_stats(False)
    st.session_state.clear()
    st.session_state['current_round'] = 1
    st.session_state['total_score'] = 0