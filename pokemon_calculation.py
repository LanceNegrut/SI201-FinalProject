#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"

# Brandon
import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt

def calculate_pokemon_total_per_year(conn):

    """
    Calculate the total number of cards of all Pokémon creature cards released each year
    
    Args: Pending"""
    
    
    cursor = conn.cursor()
    
    #creature cards (Supertype = 'Pokémon') with release dates (example from Discussion 12)
    cursor.execute("""
        SELECT releaseDate, COUNT(DISTINCT card_id) 
        FROM pokemon_cards 
        WHERE Supertype = 'Pokémon'
        GROUP BY releaseDate
    """)
    
    results = cursor.fetchall()
    
    # This would be the results into year-based dictionary (example from Discussion 12)
    year_counts = defaultdict(int)
    for date_str, count in results:
        if date_str:  # Make sure date exists
            year = date_str.split('-')[0]  # Extract year from date
            year_counts[year] += count
    
    return dict(year_counts)

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