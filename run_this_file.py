# Lance


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
    pokemon_collection.read_data_from_file()
    pokemon_collection.set_up_supertypes_table(json_data, cur, conn)
    conn.close()


if __name__ == "__main__":
    main()