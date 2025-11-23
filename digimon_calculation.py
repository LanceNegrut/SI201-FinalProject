#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"

# Brandon

import sqlite3
from {file} import {filename}


def calculate_digimon_creatures_per_year(conn):
    """
    Calculate the number of unique Digimon creature cards released each year
    
    Args:
        conn: SQLite database connection
        
    Returns:
        dict: {year: count} - Number of creature cards per year
    """
    cursor = conn.cursor()
    
    # This would get Digimon cards with date_added
    cursor.execute("""
        SELECT date_added, COUNT(DISTINCT card_id) 
        FROM digimon_cards 
        WHERE Type = 'Digimon'
        GROUP BY date_added
    """)
    
    results = cursor.fetchall()
    
    # Process results into year-based dictionary
    year_counts = defaultdict(int)
    for date_str, count in results:
        if date_str:
            year = date_str.split('-')[0]
            year_counts[year] += count
    
    return dict(year_counts)