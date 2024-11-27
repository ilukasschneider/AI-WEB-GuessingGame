import json
import os
import random
import time
import random

# utils imports
from utils import compare_traits
from utils import uncover_card
from utils import save_game_stats
from utils import GUESS_COUNT

# Streamlit-specific imports
import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space
from streamlit_js_eval import streamlit_js_eval
from streamlit_extras.stylable_container import stylable_container

# API-specific imports
from openai import OpenAI


# ------------- GLOBAL VARIABLES ------------- #
# Open-AI Api key
API_KEY = st.secrets["OPEN-AI-KEY"]

USE_CHATGPT = True



# ------------ SESSIONSTATE-VARIABLES -------------- #
def init_session_state(animal_names):

    # solution of the game
    if 'winner' not in st.session_state:
        st.session_state['winner'] = animal_names[random.randint(0, len(animal_names) - 1)]
    # count how many clues already have been used
    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0

    if 'user_guess' not in st.session_state:
        st.session_state['user_guess'] = ''

    if 'user_guess_history' not in st.session_state:
        st.session_state['user_guess_history'] = []

    if 'game_over' not in st.session_state:
        st.session_state['game_over'] = False

    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = None

    if 'clue_cards' not in st.session_state:
        st.session_state['clue_cards'] = []

    if 'clue_comments' not in st.session_state:
        st.session_state['clue_comments'] = []

    if 'won' not in st.session_state:
        st.session_state['won'] = False

    if 'sharedNumberTraitsHistory' not in st.session_state:
        st.session_state['sharedNumberTraitsHistory'] = []

# ------------- OpenAI ------------- #
# returns a generated comment for a clue via openai-api
def generateClueComment(clueNumber, guess, correctAnswer):

    client = OpenAI(api_key=API_KEY)
    model = "gpt-4o-mini"
    question = f"User's guess {clueNumber}: '{guess}'. Correct answer: '{correctAnswer}'. Write a very short comment to the user about their guess, maybe include a fun fact about '{guess}'. Keep it concise and do not give any hints about '{correctAnswer}'. Use emojis."

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question},
        ],
    )

    return(chat_completion.choices[0].message.content)


# returns a hint generated by ChatGPT
def generateHint():

    client = OpenAI(api_key=API_KEY)
    model = "gpt-4o-mini"
    prompt = (f"We are playing an animal guessing game, the correct answer is {st.session_state['winner']}. The user guessed {st.session_state['user_guess']} . Give a hint to the solution without naming the solution {st.session_state['winner']}. You can e.g. tell them about their skin or colour or the first letter of the animal but remember it is very important that your answer does not include the word {st.session_state['winner']}.")

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    answer = chat_completion.choices[0].message.content

    for word in answer.split(" "):
        yield word + " "
        time.sleep(0.2)


# returns a generated comment-stream (!) for a clue via openai-api and also saves the comment inside clueComments array
def streamAndSafeClueComment(clueNumber):
    # appends the GPT-generated comment to the gobal clueComments array
    if st.session_state['clue_comments']:
        st.session_state['clue_comments'].append(generateClueComment(clueNumber, f"{st.session_state['user_guess']}", f"{st.session_state['winner']}"))
    else:
        st.session_state['clue_comments'] = [generateClueComment(clueNumber, f"{st.session_state['user_guess']}", f"{st.session_state['winner']}")]
    # this is how this text streaming is done in streamlit
    for word in st.session_state['clue_comments'][clueNumber].split(" "):
        yield word + " "


# try to use for text input
def show_prompt():
    code = """
    let userResponse = prompt("Please enter your question about the animal:");
    if (userResponse) {
        Streamlit.setComponentValue(userResponse); // Send the response back to Streamlit
    }
    """
    result = streamlit_js_eval(code)
    return result


# ------------- RENDERING THE GAME ------------- #
def render_dev_solution():
    st.write(f"for dev correct guess: {st.session_state['winner']}")
    st.title("Animal Guessing Game")


def render_post_game():
    if st.session_state['user_guess'] == st.session_state['winner']:
        st.write("Congratulations! You won the game!")
        st.write(f"You are rewarded {GUESS_COUNT - st.session_state['counter']} points.")
        save_game_stats(st.session_state['counter'], True, st.session_state['sharedNumberTraitsHistory'])
    else:
        st.write("Game over! You lost!")
        st.write("You are rewarded 0 points.")
        save_game_stats(st.session_state['counter'], False, st.session_state['sharedNumberTraitsHistory'])


def render_game_over(selectbox_placeholder):
    selectbox_placeholder.empty()
    st.session_state['game_over'] = True
    save_game_stats(st.session_state['counter'], False, st.session_state['sharedNumberTraitsHistory'])
    st.write("Game over! You lost!")
    st.write("You are rewarded 0 points.")


def render_correct_guess(selectbox_placeholder):
    save_game_stats(st.session_state['counter'], True, st.session_state['sharedNumberTraitsHistory'])
    # hides selectbox
    selectbox_placeholder.empty()
    st.write("Congratulations! You won the game!")
    st.write(f"You are rewarded {GUESS_COUNT - st.session_state['counter']} points.")
    st.session_state['game_over'] = True
    st.session_state['won'] = True
    st.balloons()


def render_ai_comment(clue):
    # Get a cute comment by ChatGPT
    with st.chat_message("ai"):
        if len(st.session_state['clue_comments']) <= clue:
            st.write_stream(streamAndSafeClueComment(clue))
        else:
            st.write(st.session_state['clue_comments'][clue])


def render_clue_container(clue, borderColor):
    with stylable_container(
            key=f"container_with_border_{clue}",
            css_styles=f"""
                {{
                    border: 1px solid {borderColor};
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px)
                }}
                """,
        ):
        st.title(f"Clue {clue+1}")
        st.header(f"your guess was :red[{st.session_state['user_guess_history'][clue]}]")
        space(lines=2)
        st.header("shared traits are ")
        space()
        # using util function to render cards based on shared traits
        uncover_card(st.session_state['clue_cards'][clue])
        space(lines=2)

        if USE_CHATGPT: render_ai_comment(clue)

        space(lines=2)


def render_clues():
    # RENDERING CLUES ------------
    # get shared traits via util function and store values in clue_cards variable
    shared = compare_traits(st.session_state['winner'], st.session_state['user_guess'])
    st.session_state['clue_cards'].append(shared)
    # appends user guess to array for history
    st.session_state['user_guess_history'].append(st.session_state['user_guess'])
    # appends number of shared traits for coloring the border of the clue card correctly
    st.session_state['sharedNumberTraitsHistory'].append(len(shared))
    # renders clue cards in reversed order based on the guesses made
    for clue in reversed(range(st.session_state['counter'])):
        borderColor = "rgba(255, 255, 255, 1)"
        # changing boarder color of clue based on number of shared traits
        if st.session_state['sharedNumberTraitsHistory'][clue] == 0:
            borderColor = "rgba(255, 0, 0, 1)"  # red
        if st.session_state['sharedNumberTraitsHistory'][clue] == 1:
            borderColor = "rgba(255, 165, 0, 1)"  # orange
        if st.session_state['sharedNumberTraitsHistory'][clue] == 2:
            borderColor = "rgba(255, 255, 0, 1)"  # yellow
        if st.session_state['sharedNumberTraitsHistory'][clue] == 3:
            borderColor = "rgba(0, 255, 0, 1)"  # green

        render_clue_container(clue, borderColor)


def render_last_hint():
    # Generate a hint
    st.text("Here is a little hint for your last guess:")
    with st.chat_message("ai"):
        st.write(generateHint())


def render_wrong_guess(selectbox_placeholder):
    st.session_state['counter'] += 1
    # calculate guesses left
    guesses_left = GUESS_COUNT - st.session_state['counter']

    # ------------ User has still guesses left
    if guesses_left > 0:
        # ------------ User has more than 1 guess left
        if guesses_left > 1:
            st.info(f"You have {guesses_left} guesses left.")
        # ------------ User has only 1 guess left -> special hint
        else:
            st.info("This is your last guess! Use it well")
            if USE_CHATGPT: render_last_hint()
    #  ------------ User has no more guesses left
    else:
        render_game_over(selectbox_placeholder)

    render_clues()


def render_next_guess(selectbox_placeholder, animal_names):
    # Dropdown for the user to select an animal name for guessing
    st.session_state['user_guess'] = selectbox_placeholder.selectbox(
        "What animal do you think this is?",
        [""]+animal_names
    )

    # ------------ User selected an animal name
    if st.session_state['user_guess']:
        # correct guess
        if st.session_state['user_guess'] == st.session_state['winner']:
            render_correct_guess(selectbox_placeholder)
        # incorrect guess
        else:
            render_wrong_guess(selectbox_placeholder)


def render_next_round(animal_names):

    # Create a placeholder for the selectbox -> important to let it disappear after the game is over
    selectbox_placeholder = st.empty()
    # ------------ User still has guesses left
    if st.session_state['counter'] < GUESS_COUNT:
        render_next_guess(selectbox_placeholder, animal_names)
    # ------------ User has no more guesses left
    else:
        render_game_over(selectbox_placeholder)


def render_game(animal_names):
    st.image("logo.png")
    space(lines=2)

    # Check if the game is over - won or lost
    if st.session_state['game_over']:
        render_post_game()
    else:
        render_next_round(animal_names)


def render_play_again_button():
    if st.session_state['won'] or st.session_state["game_over"]:
        if st.button("Play again"):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")


def render_give_up_button():
    # you may only give up if you made at least one guess
    if st.session_state['counter'] >= 1:
        if st.sidebar.button("give up current quiz and count as loss"):
            save_game_stats(st.session_state['counter'], False, st.session_state['sharedNumberTraitsHistory'])
            # reload the page
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

def render_game_rules_expander():
    st.sidebar.divider()
    with st.sidebar.expander("Game Rules", expanded=False):
        st.write("**Welcome to the Animal Clues!**")

        st.write("### How to Play:")
        st.write(f"1. **Objective**: Guess the correct animal within {GUESS_COUNT} attempts.")
        st.write("2. **Making a Guess**:")
        st.write("   - After each guess, you'll receive clues about shared traits with the correct animal.")

        st.write("### Scoring System:")
        st.write("1. **Earning Points**:")
        st.write("   - The fewer guesses you use, the more points you earn.")
        st.write("   - The quality of each guess is also accounted for and is based on the number of shared traits. The maximum shared traits is 4.")
        st.write("2. **Winning the Game**:")
        st.write("   - Guess the correct animal to win and earn points based on remaining guesses.")
        st.write("3. **Losing the Game**:")
        st.write(f"   - If you use all {GUESS_COUNT} guesses without finding the correct animal, you lose.")

        st.write("**Good luck and have fun!**")


def start_game():

    # List of all animal names for the guessing input
    animal_names = sorted([animal['name'] for animal in json.load(open(r'animals.json', 'r'))])

    init_session_state(animal_names)

    render_game(animal_names)

    render_play_again_button()

    render_give_up_button()

    render_game_rules_expander()


start_game()
