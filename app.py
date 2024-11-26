import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils import load_game_stats, save_game_stats

# creates navigation for pages
pages = {
    "CreatureClues": [
        st.Page("game.py", title="random quiz"),
        st.Page("stats.py", title="my stats"),
        st.Page("timer.py", title="timer"),
    ],
}

pg = st.navigation(pages)

pg.run()
