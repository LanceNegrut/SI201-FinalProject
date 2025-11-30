# Lance

import requests
import sqlite3

def initialize_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # Foreign keys need to be explicitly turned on

    # TABLE 1: Pokemon Release Dates (releaseDate_id, releaseDate)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Pokemon Release Dates" (
        releaseDate_id INTEGER PRIMARY KEY,
        releaseDate TEXT UNIQUE NOT NULL
    );
    """)

    # TABLE 2: Pokemon Sets (set_id, total, releaseDate_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Pokemon Sets" (
        set_id INTEGER PRIMARY KEY,
        total INTEGER,
        releaseDate_id INTEGER,
        FOREIGN KEY (releaseDate_id) 
            REFERENCES "Pokemon Release Dates" (releaseDate_id)
    );
    """)
    
    conn.commit()
    return conn


def get_current_state(cursor):
    # Discovering how many sets are currently in the database
    cursor.execute('SELECT COUNT(set_id) FROM "Pokemon Sets"')
    total_sets = cursor.fetchone()[0]
    return total_sets


def fetch_and_insert_data(conn, api_key, page_number):
    # Feedback for user
    print(f"-> Fetching page {page_number} (Page Size: 25)...")
    
    # FETCHING DATA
    try:
        response = requests.get(f"https://api.pokemontcg.io/v2/sets?pageSize=25&page={page_number}") 
        response.raise_for_status()
        sets_data = response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return 0, False

    if not sets_data:
        return 0, False

    # INSERTING DATA
    cursor = conn.cursor()
    sets_inserted_count = 0

    with conn: 
        for set_info in sets_data:
            release_date = set_info.get('releaseDate')
            total = set_info.get('total')

            # Filtering out incomplete data
            if not all([release_date, total is not None]): continue

            cursor.execute("INSERT OR IGNORE INTO 'Pokemon Release Dates' (releaseDate) VALUES (?)", (release_date,))
            cursor.execute("SELECT releaseDate_id FROM 'Pokemon Release Dates' WHERE releaseDate = ?", (release_date,))
            release_date_id = cursor.fetchone()[0]

            cursor.execute("""
            INSERT OR IGNORE INTO "Pokemon Sets" (total, releaseDate_id)
            VALUES (?, ?)
            """, (total, release_date_id)) 
            
            if cursor.rowcount > 0:
                sets_inserted_count += 1

    return sets_inserted_count, True


def main():
    with sqlite3.connect("tcg_data.db") as conn:
        cursor = conn.cursor()
        initialize_db("tcg_data.db") 
        total_sets = get_current_state(cursor) 

        # Feedback for user
        print(f"DATABASE STATUS: {total_sets} sets currently stored (Target: 170)")
        if total_sets >= 170:
            print("\n" + "-" * 50)
            print("Target met. Congratulations!")
            print("-" * 50)
            return

        next_page = (total_sets // 25) + 1 
        sets_inserted, fetch_success = fetch_and_insert_data(conn, api_key, next_page)
        if sets_inserted > 0:
            new_total_sets = total_sets + sets_inserted

            # Feedback for user
            print("\n" + "-" * 50)
            print(f"Run Summary (Page {next_page}):")
            print(f"  - Inserted {sets_inserted} new sets!")
            print(f"  - Total sets in databse: {new_total_sets} out of 170")
            print("-" * 50)
        elif fetch_success is False and next_page > 1:
            print("\n" + "-" * 50)
            print("No more data was retrieved from the API. Data collection stopped.")
            print("-" * 50)


if __name__ == "__main__":
    main()