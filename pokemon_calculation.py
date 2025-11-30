#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"

# Brandon
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt

def calculate_pokemon_total_per_year(conn):

    """
    Calculate the total number of cards of all Pokémon creature cards released each year
    
    Args:
        conn: SQLite database connection
    Returns: 
        dict: {year: total_cards} - total cards released per year
    """
    cursor = conn.cursor()
    
    #the two tables need to be joined in order to get the releasedate. 

    cursor.execute("""
        SELECT rd.releaseDate, SUM(ps.total)
        FROM "Pokemon Release Dates" rd
        JOIN "Pokemon Sets" ps ON rd.releaseDate_id = ps.releaseDate_id
        GROUP BY rd.releaseDate
    """)
    
    results = cursor.fetchall()
    
    # This would be the results into year-based dictionary (example from Discussion 12)
    # Updating to sum total per year 
    year_counts = defaultdict(int)
    for date_str, total in results:
        if date_str and total is not None:  # Make sure date exists
            year = date_str.split('/')[0]# Extract year from date
            year_counts[year] += total
    
    return dict(year_counts)

def calculate_pokemon_sets_per_year(conn):"""

# Create a bar chart to visualize the data 

def create_histogram(data, title, xlabel, ylable):
    years = list(data.keys())
    counts = list(data.values())
    plt.bar(years, counts)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylable)
    plt.show()

    return None 