import streamlit as st
import json
import random

# Load animals from JSON file
def load_animals():
    with open('animals.json', 'r') as f:
        return json.load(f)

# Load the animal data from JSON file
animal_data = load_animals()

# Create a list of all animal names for the guessing input
animal_names = sorted([animal['name'] for group in animal_data.values() for animal in group])

# Streamlit app layout
st.title("Animal Guessing Game")

# Initialize session state for score, attempts, and rounds
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 1
if 'animal_data' not in st.session_state:
    st.session_state.animal_data = None  # Placeholder for animal data

# Display the current round and score
st.write(f"Round: {st.session_state.current_round}/5")
st.write(f"Score: {st.session_state.score}")

# Show characteristics when animal type is selected
if st.session_state.current_round <= 5:
    # Select Animal Type
    animal_type = st.selectbox("Which type of animals do you prefer?", 
                                ["Select an Option", "Carnivores", "Herbivores", "Omnivores"])

    if animal_type != "Select an Option":
        if st.session_state.animal_data is None:
            if animal_type == "Carnivores":
                filtered_animals = animal_data['carnivores']
            elif animal_type == "Herbivores":
                filtered_animals = animal_data['herbivores']
            elif animal_type == "Omnivores":
                filtered_animals = animal_data['omnivores']

            st.session_state.animal_data = random.choice(filtered_animals)

    # Access the selected animal data
    animal_data = st.session_state.animal_data

    # Proceed only if animal_data is valid
    if animal_data:
        # Initialize characteristics to show based on attempts
        if st.session_state.attempts == 0:
            traits_to_display = {
                "habitat": animal_data["characteristics"]["habitat"],
                "biggest_threat": animal_data["characteristics"]["biggest_threat"],
                "prey": animal_data["characteristics"]["prey"]
            }
        elif st.session_state.attempts == 1:
            traits_to_display = {
                "habitat": animal_data["characteristics"]["habitat"],
                "biggest_threat": animal_data["characteristics"]["biggest_threat"],
                "prey": animal_data["characteristics"]["prey"],
                "most_distinctive_feature": animal_data["characteristics"]["most_distinctive_feature"],
                "gestation_period": animal_data["characteristics"]["gestation_period"],
                "estimated_population_size": animal_data["characteristics"]["estimated_population_size"]
            }
        else:  # For the third attempt
            traits_to_display = animal_data["characteristics"]

        # Display the characteristics based on attempts as bullet points
        st.write("Here are some characteristics of the animal:")
        bullet_points = "\n".join([f"- {trait.capitalize()}: {value}" for trait, value in traits_to_display.items()])
        st.markdown(bullet_points)

        # Create a dropdown for the user to select the animal name
        user_guess = st.selectbox("What animal do you think this is?", [''] + animal_names)

        # Button to check the guess
        if st.button("Check Guess"):
            if user_guess != '':
                st.session_state.attempts += 1
                if user_guess.lower() == animal_data['name'].lower():
                    # Right answer logic
                    st.success("You are right! Good Job!")
                    if st.session_state.attempts == 1:
                        st.session_state.score += 3  # Reward for first attempt
                        st.write("You earned 3 points!")
                    elif st.session_state.attempts == 2:
                        st.session_state.score += 2  # Reward for second attempt
                        st.write("You earned 2 points!")
                    else:
                        st.session_state.score += 1  # Reward for third attempt
                        st.write("You earned 1 point!")

                    # Show the image after correct guess
                    st.image(animal_data['image'], caption=f"This is a {animal_data['name']}!", use_container_width=True)

                    # Reset for the new round
                    st.session_state.animal_data = None
                    st.session_state.attempts = 0
                    st.session_state.current_round += 1  # Move to the next round
                else:
                    # Wrong answer logic
                    remaining_attempts = 3 - st.session_state.attempts
                    if remaining_attempts > 0:
                        st.error(f"Sorry, your answer is not correct. You have {remaining_attempts} more attempts.")
                    else:
                        st.error(f"Sorry, your answer is not correct. The correct answer was: {animal_data['name']}.")
                        # Show the image if all attempts are incorrect
                        st.image(animal_data['image'], caption=f"This is a {animal_data['name']}!", use_container_width=True)

                        # Reset for the new round
                        st.session_state.animal_data = None
                        st.session_state.attempts = 0
                        st.session_state.current_round += 1  # Move to the next round

# After 5 rounds, display final score
if st.session_state.current_round > 5:
    st.success("Game Over!")
    st.write(f"Your final score is: {st.session_state.score}")
