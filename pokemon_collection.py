# Lance

import requests
import json


def get_api_key(filename):
    '''
    loads in API key from file 

    ARGUMENTS:  
        file: file that contains your API key
    
    RETURNS:
        your API key
    '''
    try:
        with open(filename, 'r') as f:
            api_key = f.read().strip()
            return api_key
    except:
        print(f"Error: The file '{filename}' was not found.")
        return None


API_KEY = get_api_key("pokemon_api_key.txt")


def load_json(filename):
    '''
    opens file file, loads content as json object

    ARGUMENTS: 
        filename: name of file to be opened

    RETURNS: 
        json dictionary OR an empty dict if the file could not be opened 
    '''
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}


def create_cache(dict, filename):
    '''
    Encodes dictonary into JSON format and writes
    the JSON to filename to save the search results

    ARGUMENTS: 
        filename: the name of the file to write a cache to
        dict: cache dictionary

    RETURNS: 
        None
    '''

    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4) 
    return None


def create_pokemon_table(db_name):
    pass