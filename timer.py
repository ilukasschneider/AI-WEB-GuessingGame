import time
import streamlit as st
# set the time limit
timer_duration = 30

if st.button("Start Timer"):
    placeholder = st.empty()  # placeholder to display some info
    for remaining in range(timer_duration, 0, -1):
        # show the remaining time
        placeholder.write(f"Time remaining: {remaining} seconds")

        # wait a second until continuing
        time.sleep(1)



    # display a message when the timer has ended
    placeholder.write("Time is up!")
    st.markdown("<h1 style='text-align: center; color: red; '>GAME OVER</h1>", unsafe_allow_html=True)
