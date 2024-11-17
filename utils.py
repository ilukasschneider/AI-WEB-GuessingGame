import json
import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space
import random

animals = json.load(open(r'betterAnimalDB\animals.json', 'r'))

#Todo:
# - deal with cases where None is returned
# - deal with locations

def get_traits(animal1, animal2):
    trait1, trait2 = None, None
    for animal in animals:
        if animal['name'] == animal1:

            trait1 = {'class': animal['taxonomy']['class'],
              'location': animal['locations'],
              'diet': animal['characteristics']['diet'],
                'habitat': animal['characteristics']['habitat'],
                      'prey': animal['characteristics']['prey'],
                      'threat': animal['characteristics']['biggest_threat']}

        elif animal['name'] == animal2:

            trait2 = {'class': animal['taxonomy']['class'],
              'location': animal['locations'],
              'diet': animal['characteristics']['diet'],
                'habitat': animal['characteristics']['habitat'],
                      'prey': animal['characteristics']['prey'],
                      'threat': animal['characteristics']['biggest_threat']}

    return trait1, trait2

def compare_traits(animal1, animal2):
    traits1, traits2 = get_traits(animal1, animal2)

    shared = {}
    for trait in traits1:
        if traits1[trait] == traits2[trait]:
            shared[trait] = traits1[trait]

    return shared

def uncover_card(shared_traits, i):
    if shared_traits:
        topCols = st.columns(len(shared_traits[i])//2)
        buttonCols = -1
        if len(shared_traits[i])%2 != 0:
            buttonCols = st.columns(1)


        for i in range(topCols):
            with topCols[i]:
                key = next(iter(shared_traits))
                ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        for i in range(buttonCols):
            with buttonCols[i]:
                key = next(iter(shared_traits))
                ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        space()
    else:
        st.title("Unfortunately no commonalities")


