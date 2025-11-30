# Lance

import requests
import sqlite3

def initialize_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # Foreign keys need to be explicitly turned on

    # TABLE 1: Yu-Gi-Oh Release Dates (tcg_date_id, tcg_date)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Yu-Gi-Oh Release Dates" (
        tcg_date_id INTEGER PRIMARY KEY,
        tcg_date TEXT UNIQUE NOT NULL
    );
    """)

    # TABLE 2: Yu-Gi-Oh Sets (set_id, num_of_cards, tcg_date_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Yu-Gi-Oh Sets" (
        set_id INTEGER PRIMARY KEY,
        set_name TEXT,
        num_of_cards INTEGER,
        tcg_date_id INTEGER,
        FOREIGN KEY (tcg_date_id) 
            REFERENCES "Yu-Gi-Oh Release Dates" (tcg_date_id)
        UNIQUE(set_name, tcg_date_id)
    );
    """)
    
    conn.commit()
    return conn


def get_current_state(cursor):
    # Discovering how many sets are currently in the database
    cursor.execute('SELECT COUNT(set_id) FROM "Yu-Gi-Oh Sets"')
    total_sets = cursor.fetchone()[0]
    return total_sets


def fetch_and_insert_data(conn, page_number, limit):
    # Feedback for user
    print(f"-> Fetching page {page_number} (Page Size: 25)...")
    
    # FETCHING DATA
    try:
        response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardsets.php") 
        response.raise_for_status()
        all_sets = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return 0, False

    if not all_sets:
        return 0, False

    start_index = (page_number - 1) * 25
    
    # Don't add anything if all the sets are already there
    if start_index >= len(all_sets):
        return 0, False

    # INSERTING DATA
    cursor = conn.cursor()
    sets_inserted_count = 0
    current_index = start_index

    with conn: 
        while sets_inserted_count < limit and current_index < len(all_sets):
            set_info = all_sets[current_index]
            current_index += 1
            set_name = set_info.get('set_name')
            tcg_date = set_info.get('tcg_date')
            num_of_cards = set_info.get('num_of_cards')
            
            # Filtering out incomplete data
            if not all([set_name, tcg_date, num_of_cards is not None]): continue

            cursor.execute("INSERT OR IGNORE INTO 'Yu-Gi-Oh Release Dates' (tcg_date) VALUES (?)", (tcg_date,))
            cursor.execute("SELECT tcg_date_id FROM 'Yu-Gi-Oh Release Dates' WHERE tcg_date = ?", (tcg_date,))
            tcg_date_id = cursor.fetchone()[0]

            cursor.execute("""
            INSERT OR IGNORE INTO "Yu-Gi-Oh Sets" (set_name, num_of_cards, tcg_date_id)
            VALUES (?, ?, ?)
            """, (set_name, num_of_cards, tcg_date_id)) 
            
            if cursor.rowcount > 0:
                sets_inserted_count += 1

    return sets_inserted_count, True


def main():
    with sqlite3.connect("tcg_data.db") as conn:
        cursor = conn.cursor()
        initialize_db("tcg_data.db") 
        total_sets = get_current_state(cursor) 

        # Feedback for user
        print(f"DATABASE STATUS: {total_sets} sets currently stored (Target: 1006)")
        if total_sets >= 1006:
            print("\n" + "-" * 50)
            print("Target met. Congratulations!")
            print("-" * 50)
            return

        next_page = (total_sets // 25) + 1
        
        # Preventing insertion of extra rows
        items_needed = 1006 - total_sets
        limit = min(25, items_needed)

        sets_inserted, fetch_success = fetch_and_insert_data(conn, next_page, limit)
        if sets_inserted > 0:
            new_total_sets = total_sets + sets_inserted

            # Feedback for user
            print("\n" + "-" * 50)
            print(f"Run Summary (Page {next_page}):")
            print(f"  - Inserted {sets_inserted} new sets!")
            print(f"  - Total sets in databse: {new_total_sets} out of 1006")
            print("-" * 50)
        elif fetch_success is False and next_page > 1:
            print("\n" + "-" * 50)
            print("No more data was retrieved from the API. Data collection stopped.")
            print("-" * 50)


if __name__ == "__main__":
    main()