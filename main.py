""" This repository is for the purpose of learning how to use WikiData and SPARQL. My thesis
includes learning the entities behind the title and abstract of a news article because it is
the format the MIND dataset is in.
"""

import spacy
import requests
TEST_START = True

def search_wiki(search_term):
    """ Search for entities with the label "search_term" """
    search_link = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&search={search_term}&format=json"
    search_results = requests.get(search_link).json()
    return search_results

def get_entity_id(search_results):
    """ Get the entity ID of the first result """
    return search_results["search"][0]["id"]

def get_entity_url(entity_id):
    """ Get the URL of the entity """
    return f"https://www.wikidata.org/wiki/{entity_id}"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """ Extract entities from text """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def print_entities(entities):
    for entity in entities:
        # We get entity[0] because it's a tuple
        search = search_wiki(entity[0])
        if len(search["search"]) > 0:
            entity_id = get_entity_id(search)
            entity_url = get_entity_url(entity_id)

            print_string = f"Entity: {entity[0]}\nEntity ID: {entity_id}\nEntity URL: {entity_url}\n"
            print(print_string)
        else:
            print(f"No entity found for {entity[0]}\n")

if TEST_START:
    sample_text = "Mike Tomlin: Steelers ‘accept responsibility’ for role in brawl with Browns"

    # Extract entities
    entities = extract_entities(sample_text)

    # Print entities
    print(str(entities)+"\n")

    # Print entities with ID and URL
    print_entities(entities)

# Loop to let user type a title or term to search
running = True
while running:
    search_term = input("(type q to exit) Enter a title or term to search: ")
    if search_term == "q":
        running = False
        break

    entities = extract_entities(search_term)
    if len(entities) > 0:
        print(f"Entities found: {str(entities)}\n")

        # Print entities with ID and URL
        print_entities(entities)
    else:
        print("No entities found.\n")

    # Ask if user wants to search again
    search_again = input("Search again? (y/n): ")
    if search_again == "n":
        running = False
