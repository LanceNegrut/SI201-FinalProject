# Lance

import pokemon_collection
import pokemon_calculation
import yugioh_collection
import yugioh_calculation
import digimon_collection
import digimon_calculation
import sqlite3
import os


def set_up_database(db_name):
    """
    Sets up a SQLite database connection and cursor.

    Parameters
    -----------------------
    db_name: str
        The name of the SQLite database.

    Returns
    -----------------------
    Tuple (Cursor, Connection):
        A tuple containing the database cursor and connection objects.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    set_up_database("tcg_data")
    API_KEY = pokemon_collection.get_api_key("pokemon_api_key.txt")
    pokemon_collection.load_json(filename)
    pokemon_collection.create_cache(filename)
    pokemon_collection.read_data_from_file(filename)
    pokemon_collection.set_up_supertypes_table(json_data, "tcg_data", conn)
    conn.close()


if __name__ == "__main__":
    main()