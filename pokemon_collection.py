# Lance

import requests
import sqlite3
import json
import os


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


def read_data_from_file(filename):
    """
    Reads data from a file with the given filename.

    Parameters
    -----------------------
    filename: str
        The name of the file to read.

    Returns
    -----------------------
    dict:
        Parsed JSON data from the file.
    """
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data


def set_up_types_table(data, cur, conn):
    """
    Sets up the Types table in the database using the provided Pokemon data.

    Parameters
    -----------------------
    data: list
        List of Pokemon data in JSON format.

    cur: Cursor
        The database cursor object.

    conn: Connection
        The database connection object.

    Returns
    -----------------------
    None
    """
    type_list = []
    for pokemon in data:
        pokemon_type = pokemon["type"][0]
        if pokemon_type not in type_list:
            type_list.append(pokemon_type)
        if len(pokemon["type"]) > 1:
            pokemon_type = pokemon["type"][1]
            if pokemon_type not in type_list:
                type_list.append(pokemon_type)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)"
    )
    for i in range(len(type_list)):
        cur.execute(
            "INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)", (i,
                                                                   type_list[i])
        )
    conn.commit()