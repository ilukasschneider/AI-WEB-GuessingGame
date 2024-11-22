import requests
import json
import time
from dotenv import load_dotenv
import os
load_dotenv()

API_URL = 'https://api.api-ninjas.com/v1/animals'
API_KEY = os.getenv("ANIMAL-KEY")


with open('animal_names.txt', 'r') as file:
    animal_names = [line.strip() for line in file.readlines()]

animals = []

headers = {
    'X-Api-Key': API_KEY
}

for name in animal_names:
    params = {
        'name': name
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == requests.codes.ok:
        data = response.json()
        if data:
            animals.extend(data)
            print(f'Fetched data for {name}')
        else:
            print(f'No data found for {name}')
    else:
        print("Error:", response.status_code, response.text)
    time.sleep(1)

with open('animals.json', 'w') as f:
    json.dump(animals, f, indent=2)
