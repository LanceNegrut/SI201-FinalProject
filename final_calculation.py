#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"


# Brandon

import sqlite3
import matplotlib.pyplot as plt
from pokemon_calculation import calculate_pokemon_creatures_per_year
from digimon_calculation import calculate_digimon_creatures_per_year
from yugioh_calculation import calculate_yugioh_creatures_per_year
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

    all_year = set(pokemon_data.keys()), set(yugio_data.keys()), set(digimon_data.keys())

    return all_year
    
    count = 0
    for year in all_year:
        total = pokemon_data.get(year, 0) + #pending...


    


    



