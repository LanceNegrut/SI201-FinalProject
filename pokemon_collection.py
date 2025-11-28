# Lance

import requests
import sqlite3

# Configuration variables are derived implicitly from main() calls

def get_api_key(filename):
    """Reads the API key from the separate .txt file."""
    try:
        with open(filename, 'r') as f:
            key = f.readline().strip()
            if not key: raise ValueError("API key file is empty.")
            return key
    except Exception as e:
        print(f"Error accessing API key file '{filename}': {e}")
        exit(1)

def initialize_db(db_name):
    """Connects to/creates the DB, and sets up tables (Config table removed)."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # Enforce FKs

    # 1. Pokemon Release Dates Table (Parent: releaseDate_id, releaseDate)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Pokemon Release Dates" (
        releaseDate_id INTEGER PRIMARY KEY,
        releaseDate TEXT UNIQUE NOT NULL
    );
    """)

    # 2. Pokemon Sets Table (Child: set_id, name, total, releaseDate_id FK)
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
    # Count the rows in the main data table to determine progress.
    cursor.execute('SELECT COUNT(set_id) FROM "Pokemon Sets"')
    total_sets = cursor.fetchone()[0]
    return 0, total_sets # Returns 0 for the obsolete 'last_page' variable

def fetch_and_insert_data(conn, api_key, page_number):
    """Fetches a page of data and inserts unique records into the database."""

    url = f"https://api.pokemontcg.io/v2/sets?pageSize=25&page={page_number}"
    headers = {'X-Api-Key': api_key}
    
    print(f"-> Fetching page {page_number} (Page Size: 25)...")
    
    # --- Fetch Data ---
    try:
        response = requests.get(url, headers=headers) 
        response.raise_for_status()
        sets_data = response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return 0, False

    if not sets_data:
        return 0, False

    # --- Insert Data ---
    cursor = conn.cursor()
    sets_inserted_count = 0

    # OPTIMIZATION: Use an explicit transaction context manager (recommended for performance)
    with conn: 
        for set_info in sets_data:
            release_date = set_info.get('releaseDate')
            total = set_info.get('total')

            if not all([release_date, total is not None]): continue

            # 1. Insert/Get releaseDate_id (Parent)
            cursor.execute("INSERT OR IGNORE INTO 'Pokemon Release Dates' (releaseDate) VALUES (?)", (release_date,))
            cursor.execute("SELECT releaseDate_id FROM 'Pokemon Release Dates' WHERE releaseDate = ?", (release_date,))
            release_date_id = cursor.fetchone()[0]

            # 2. Insert set details (Child) - INSERT OR IGNORE relies on 'name' being UNIQUE
            cursor.execute("""
            INSERT OR IGNORE INTO "Pokemon Sets" (total, releaseDate_id)
            VALUES (?, ?)
            """, (total, release_date_id)) 
            
            if cursor.rowcount > 0:
                sets_inserted_count += 1
            
    # The 'with conn' block handles the commit/rollback, improving performance.
    return sets_inserted_count, True


def main():
    """Controls the incremental data collection process across multiple runs."""

    api_key = get_api_key("pokemon_api_key.txt")
    
    # Automatic closing
    with sqlite3.connect("tcg_data.db") as conn:
        cursor = conn.cursor()
        
        # Initialize tables
        initialize_db("tcg_data.db") 
        
        # Get total sets by counting rows
        _, total_sets = get_current_state(cursor) 

        print(f"**Database Status:** {total_sets} sets currently stored (Target: 100)")

        # Calculate next_page based on stored data count.
        next_page = (total_sets // 25) + 1 
        
        # Combined Fetch and Insert Step
        sets_inserted, fetch_success = fetch_and_insert_data(conn, api_key, next_page)
        
        if sets_inserted > 0:
            # The fetch_and_insert_data function handles the commit
            
            # Recalculate new total
            new_total_sets = total_sets + sets_inserted

            print("\n" + "-" * 50)
            print(f"**Run Summary (Page {next_page}):**")
            print(f"  - Inserted {sets_inserted} new unique set records.")
            print(f"  - Total sets stored: {new_total_sets}")
            print(f"  - Remaining until target: {max(0, 100 - new_total_sets)}")
            print("-" * 50)
        elif fetch_success is False and next_page > 1:
            print("\n" + "-" * 50)
            print("No more data was retrieved from the API. Data collection stopped.")
            print("-" * 50)


if __name__ == "__main__":
    main()