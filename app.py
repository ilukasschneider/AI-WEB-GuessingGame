import streamlit as st

# creates navigation for pages
pages = {
    "CreatureClues": [
        st.Page("game.py", title="random quiz"),
        st.Page("stats.py", title="stats"),
    ],
}


st.sidebar.button("give up")
pg = st.navigation(pages)


pg.run()
