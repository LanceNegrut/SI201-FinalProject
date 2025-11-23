# Lance

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

def load_json(filename):
    pass

def create_cache(dict, filename):
    pass

def create_pokemon_table(db_name):
    pass