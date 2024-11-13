import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space
import random
import time
from dotenv import load_dotenv
import os
from openai import OpenAI

# loads the .env file
load_dotenv()
# counts the number of current clues
clueCount = 3
# stores the comments for each clue // should be later used to safe GPT-generated answers as cookies so they dont get lost when refreshing the page
clueComments = []
# stores shared traits for each clue
sharedTraits = [["water", "wings", "2", "4"],["-", "-", "5", "-"],["flying", "wings", "-", "4"]]

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


# returns a generated comment for a clue via openai-api and also saves the comment inside clueComments array
def streamAndSafeClueComment(clueNumber):
    clueComments.append(generateClueComment(clueNumber, "chicken", "tiger"))
    for word in clueComments[clueNumber].split(" "):
        yield word + " "
        time.sleep(0.01)


# renders clues based on clueCount and generates a new comment if a comment for a clue is missing/not yet generated yet
for i in range(clueCount):
    commonTraitCount = 0
    for item in sharedTraits[i]:
        if item != "-":
            commonTraitCount += 1
    with st.container(border=True):
        st.title(f"clue {i+1}")
        if commonTraitCount > 1:
            st.header("your guess was: :orange[chicken]")
        else:
            st.header("your guess was: :red[chicken]")
        space()
        space()
        topCols = st.columns(2)
        buttonCols = st.columns(2)
        with topCols[0]:
            ui.metric_card(title="shared x", content=sharedTraits[i][0], key=f"card{random.randint(0, 20000)}")
        with topCols[1]:
            ui.metric_card(title="shared x", content=sharedTraits[i][1], key=f"card{random.randint(0, 20000)}")
        with buttonCols[0]:
            ui.metric_card(title="shared x", content=sharedTraits[i][2], key=f"card{random.randint(0, 20000)}")
        with buttonCols[1]:
            ui.metric_card(title="shared x", content=sharedTraits[i][3], key=f"card{random.randint(0, 20000)}")
        space()
        space()
        with st.chat_message("ai"):
            if i >= len(clueComments):
                st.write_stream(streamAndSafeClueComment(i))
            else:
                st.write(clueComments[i])
        space()
        space()
