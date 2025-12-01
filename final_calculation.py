#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"


# Brandon

import sqlite3
import matplotlib.pyplot as plt
from pokemon_calculation import calculate_pokemon_total_per_year, calculate_pokemon_sets_per_year
from yugioh_calculation import calculate_yugioh_total_per_year, calculate_yugioh_sets_per_year


def joining_tables(conn):

    """
    Join tables to combine data from Pokemon, Yu-Gi-Oh cards per year. 
    
    """

    pokemon_data = calculate_pokemon_total_per_year(conn)
    yugioh_data = calculate_yugioh_total_per_year(conn)

    all_years = set(pokemon_data.keys()) | set(yugioh_data.keys())
    combined_data = {}

    for year in all_years:
        combined_data[year] = pokemon_data.get(year, 0) + yugioh_data.get(year, 0)
    return combined_data, pokemon_data, yugioh_data

def create_histogram(pokemon_data, yugioh_data, combined_data):
    """

    Create histogram comparing Pokemon, Yu-Gi-Oh, and combined card release per year and showing the trend and differences.
    
    """

    all_years = sorted # Left on here for the next part of the code



    


    



