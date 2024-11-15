import time
import streamlit as st
# Setze die Timer-Dauer in Sekunden
timer_duration = 30

if st.button("Start Timer"):
    placeholder = st.empty()  # Platzhalter für die dynamische Timer-Anzeige
    for remaining in range(timer_duration, 0, -1):
        # Zeige den verbleibenden Timerwert
        placeholder.write(f"Zeit verbleibend: {remaining} Sekunden")

        # Warte eine Sekunde, bevor der Timer runterzählt
        time.sleep(1)



    # Zeige eine Nachricht, wenn der Timer endet
    placeholder.write("Zeit abgelaufen!")
    st.markdown("<h1 style='text-align: center; color: red; '>GAME OVER</h1>", unsafe_allow_html=True)