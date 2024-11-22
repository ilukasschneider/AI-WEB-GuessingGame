# AI-WEB-GuessingGame

Welcome to the **AI-WEB-GuessingGame** repository! This project is an interactive web-based guessing game centered on identifying animals. It is developed using **Python** and **Streamlit** as part of a university course.

## 📐 Basic Architecture

The project follows a straightforward architecture:

1. **Backend and Frontend**:
   - The web application is created using **Streamlit**, which handles both the frontend and backend seamlessly.
   - Data with animal information was fetched from the [**Animals API**](https://api-ninjas.com/api/animals).
   - Key components:
     - `game.py`: Contains the main game logic.
     - `game_stats.py`: Responsible for visualizing game statistics.
     - `utils.py`: Includes utility functions, such as calculating user scores.
     - `betterAnimalDB/animals.json`: DB for animal data.

2. **Game Logic**:
   - Users guess animals based on clues provided after each guess. Each clue highlights 1-4 shared characteristics between the guessed and the target animal.
   - The fewer guesses the user takes to identify the animal, the higher their score.
   - The quality of each guess is measured by the number of shared characteristics, with the result visually indicated by clue colors.
   - During the final guess, users can interact with (Open) AI for a hint via a chat feature.

3. **Deployment**:
   - The app can be run locally or accessed via **Streamlit Cloud** (link provided in the repository description).

## ⚙️ Requirements

To run the project locally, make sure you have the following installed:

1. **Python**
   - Download from [python.org](https://www.python.org/).

2. **Streamlit**
   - Install Streamlit via pip:
     ```bash
     pip install streamlit
     ```

3. **Other Dependencies**:
   - Additional libraries are listed in the `requirements.txt` file.
   - Install them using:
     ```bash
     pip install -r requirements.txt
     ```
