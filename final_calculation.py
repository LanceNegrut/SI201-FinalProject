#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"


# Brandon

import sqlite3
import matplotlib.pyplot as plt
from pokemon_calculation.py import calculate_pokemon_creatures_per_year
from digimon_calculation.py import calculate_digimon_creatures_per_year
from yugioh_calculation.py import calculate_yugioh_creatures_per_year
import math


def joining_tables(cur):

    """
    Join tables to get complete Amount of unique creature cards released each year for each game
    
    Args:
        conn: Sqlite database connection
    
    Return 
        dict: {year: count} - number of creature cards per year"""
    
    pokemon_data = calculate_pokemon_creatures_per_year(cur)
    yugio_data = calculate_yugioh_creatures_per_year(cur)
    digimon_data = calculate_digimon_creatures_per_year(cur)

    all_year = set(pokemon_data.)
    


    



