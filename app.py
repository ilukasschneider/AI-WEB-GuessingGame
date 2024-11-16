import streamlit as st

# creates navigation for pages
pages = {
    "CreatureClues": [
        st.Page("game.py", title="random quiz"),
        st.Page("stats.py", title="my stats"),
        st.Page("timer.py", title="timer"),
    ],
}


st.sidebar.button("give up")
pg = st.navigation(pages)


pg.run()
