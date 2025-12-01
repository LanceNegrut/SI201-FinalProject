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

def calculate_pokemon_sets_per_year(conn):
    
    """
    Calculate the number of Pokémon set releases each year
    
    Args:
        conn: SQLite database connection
    Returns:
        dict: {year: count} - number of set per year
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rd.releaseDate, COUNT(ps.set_id)
        FROM "Pokemon Release Dates" rd
        JOIN "Pokemon Sets" ps ON rd.releaseDate_id = ps.releaseDate_id
        GROUP BY rd.releaseDate
        """)
    
    result = cursor.fetchall()

    year_counts = defaultdict(int)
    for date_str, count in result:
        if date_str:
            year = date_str.split('/')[0]
            year_counts[year] += count
    return dict(year_counts)

# Create a bar chart to visualize the data 

def create_histogram(data, title, xlabel, ylabel):
    """
    Create a histogram to visualize the the data

    Args:

        data: Year as key and count as value 
        title: Title of the histogram
        xlabel: x-axis 
        ylabel: y-axis 
    """
    
    years = sorted(data.keys())
    counts = [data[year] for year in years] #this is data values by year 
    #counts = list(data.values())


    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color="skyblue", edgecolor="black", linewidth=1.5)
    #plt.bar(years, counts)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()


def write_calculation_to_file(total_cards_data, sets_data, filename='pokemon_calculation.txt'):
    # Rubric write calculation result to a text file:

    """
    Write calculation result to a text file

    Args:
        total_cards_data: dict of the total cards released per year 
        sets_data: dict of the total sets released per year 
        filename: this would be the output filename 
    """

    with open(filename, 'w') as f:
        f.write("Pokemon Cards Released Per Year:\n")
        for year in sorted(total_cards_data.keys()):
            f.write(f'{year}: {total_cards_data[year]}\n')
            f.write('\n')
        f.write("Pokemon Sets Released Per Year:\n")
        for year in sorted(sets_data.keys()):
            f.write(f'{year}: {sets_data[year]}\n')
            f.write('\n')
    print(f"Calculation results written to {filename}")

def main():
    conn: sqlite3.connection = sqlite3.connect('tcg_data.db')

    pokemon_total_per_year = calculate_pokemon_total_per_year(conn)
    create_histogram(pokemon_total_per_year, "Total Pokémon Cards Released Per Year", "Year", "Total Cards Released")
    pokemon_sets_per_year = calculate_pokemon_sets_per_year(conn)
    create_histogram(pokemon_sets_per_year, "Total Pokémon Sets Released Per Year", "Year", "Total Sets Released")
    pokemon_total_per_year, pokemon_sets_per_year = calculate_pokemon_total_per_year(conn), calculate_pokemon_sets_per_year(conn)
    write_calculation_to_file(pokemon_total_per_year, pokemon_sets_per_year) # why is the text file not being created?
    
    conn.close()

if __name__ == "__main__":
    main()