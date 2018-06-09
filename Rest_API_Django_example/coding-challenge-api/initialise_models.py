import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend-api.settings')

import django
django.setup()

from paranuara.models import Companies_db, People_db
import json

# Read json files
def read_json(data_dir):
    with open(data_dir, 'r') as json_file:
         json_data = json.load(json_file)
    return json_data

# Initalise and populate Django model values with the provided json data
def initialise_django_db(companies_data, people_data):
    
    # Populate people data into People_db model
    for person in people_data:
        People_db.objects.get_or_create(
            _id=person['_id'],
            index=person['index'],
            guid=person['guid'],
            has_died=person['has_died'],
            balance=person['balance'],
            picture=person['picture'],
            age=person['age'],
            eye_color=person['eyeColor'],
            name=person['name'],
            gender=person['gender'],
            company_id=person['company_id'],
            email=person['email'],
            phone=person['phone'],
            address=person['address'],
            about=person['about'],
            registered=person['registered'],
            tags=person['tags'],
            friends=person['friends'],
            greeting=person['greeting'],
            favourite_food=person['favouriteFood']       
        )

    # Populate companies data into Companies_db model
    for company in companies_data:
        Companies_db.objects.get_or_create(
            index=company['index'],
            company_name=company['company']       
        )

# Main script
if __name__ == '__main__':
    print("\n--------Initialise Django model with json data-------")
    # Set the directory for the data file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PEOPLE_DATA_DIR = os.path.join(BASE_DIR, 'coding-challenge-api', 'static', 'data', 'people.json')
    COMPANIES_DATA_DIR = os.path.join(BASE_DIR, 'coding-challenge-api', 'static', 'data', 'companies.json')
    people_data = read_json(PEOPLE_DATA_DIR)
    companies_data = read_json(COMPANIES_DATA_DIR)

    # Save data into Django models
    initialise_django_db(companies_data, people_data)
    
    print('Task completed!')