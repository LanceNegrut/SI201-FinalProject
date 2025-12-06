#Calculation in one file: 

#Brandon will be working on it this: 

#Double check this file task is for Brandon's "calculation"

#combining both pokemon and yugioh calculation into one file as a final calculation file. Then we delete those files. 

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

def create_pokemon_histogram(data, title, xlabel, ylabel):
    """
    Create a histogram to visualize the the data for Pokemon

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


    #THIS WOULD BE THE YU_GI_OH CALCULATION PART 

def calculate_yugioh_total_per_year(conn):

    """
    Calculate the total number of cards of all Yu-Gi-Oh creature cards released each year
    
    Args:
        conn: SQLite database connection
    Returns: 
        dict: {year: total_cards} - total cards released per year
    """
    cursor = conn.cursor()
    
    #the two tables need to be joined in order to get the releasedate. 

    cursor.execute("""
        SELECT rd.tcg_date, SUM(ps.num_of_cards)
        FROM "Yu-Gi-Oh Release Dates" rd
        JOIN "Yu-Gi-Oh Sets" ps ON rd.tcg_date_id = ps.tcg_date_id
        GROUP BY rd.tcg_date
    """)
    
    results = cursor.fetchall()
    
    # This would be the results into year-based dictionary (example from Discussion 12)
    # Updating to sum total per year 
    year_counts = defaultdict(int)
    for date_str, total in results:
        if date_str and total is not None:  # Make sure date exists
            year = date_str.split('-')[0]# Extract year from date
            year_counts[year] += total
    
    return dict(year_counts)

def calculate_yugioh_sets_per_year(conn):
    
    """
    Calculate the number of Yu-Gi-Oh set releases each year
    
    Args:
        conn: SQLite database connection
    Returns:
        dict: {year: count} - number of set per year
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rd.tcg_date, COUNT(ps.set_id)
        FROM "Yu-Gi-Oh Release Dates" rd
        JOIN "Yu-Gi-Oh Sets" ps ON rd.tcg_date_id = ps.tcg_date_id
        GROUP BY rd.tcg_date
        """)
    
    result = cursor.fetchall()

    year_counts = defaultdict(int)
    for date_str, count in result:
        if date_str:
            year = date_str.split('-')[0]
            year_counts[year] += count
    return dict(year_counts)


    #THIS PART WOULD BE THE HISOTOGRAM PART FOR YU-GI-OH

def create_yugioh_histogram(data, title, xlabel, ylabel):
    """
    Create a histogram to visualize the the data for Yu-Gi-Oh

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


def joining_tables(conn):

    """
    Join tables to combine data from Pokemon, Yu-Gi-Oh cards per year. 

    Returns: 
    tuple with combined data, pokemon data, yugioh data
    
    """

    pokemon_data = calculate_pokemon_total_per_year(conn)
    yugioh_data = calculate_yugioh_total_per_year(conn)

    all_years = set(pokemon_data.keys()) | set(yugioh_data.keys())
    combined_data = {}

    for year in all_years:
        combined_data[year] = pokemon_data.get(year, 0) + yugioh_data.get(year, 0)
    return combined_data, pokemon_data, yugioh_data

def create_combined_histogram(pokemon_data, yugioh_data, combined_data):
    """

    Create histogram comparing Pokemon, Yu-Gi-Oh, and combined card release per year and showing the trend and differences.
    
    """

    all_years = sorted(set(pokemon_data.keys()) | set(yugioh_data.keys()))

    pokemon_values = [pokemon_data.get(year, 0) for year in all_years]
    yugioh_values= [yugioh_data.get(year, 0) for year in all_years]
    combined_values = [combined_data.get(year, 0) for year in all_years]

    x = np.arange(len(all_years))
    width = 0.25

    bars1 = plt.bar(x - width, pokemon_values, width, label='Pokemon', color='blue', edgecolor='black', linewidth=1.5)
    bars2 = plt.bar(x, yugioh_values, width, label='Yu-Gi-Oh', color='red', edgecolor='black', linewidth=1.5)
    bars3 = plt.bar(x + width, combined_values, width, label='Combined', color='yellow', edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax.set_ylabel('Total Cards Released', fontsize=13, fontweight='bold')
    ax.set_title('TCG Production Trends: Pokemon vs Yu-Gi-Oh Over the Years', fontsize=16, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(all_years, rotation=45, ha='right')
    ax.legend(axis='y', alpha=0.7, linestyle="--")

    plt.tight_laoyout()
    plt.show()


def calculate_average_cards_per_set(conn):
    """
    We are going to get the avarege cards per set for each year.
    SHow the trend: Sets getting bigger or smaller over time.

    Returns:
    tuple: (pokemon_avg_per_set, yugioh_avg_per_set)

    """

    pokemon_cards = calculate_pokemon_total_per_year(conn)
    pokemont_sets = calculate_pokemon_sets_per_year(conn)
    yugioh_cards = calculate_yugioh_total_per_year(conn)
    yugioh_sets = calculate_yugioh_sets_per_year(conn)

    pass 



def write_calculation_to_file(pokemon_total_cards, pokemon_sets, yugioh_total_cards, yugioh_sets, filename='All_calculation.txt'):
    # Rubric write calculation result to a text file:

    """
    Write calculation result to a text file with both Pokemon and Yu-Gi-Oh data

    Args:
        total_cards_data: dict of the total cards released per year 
        sets_data: dict of the total sets released per year 
        filename: this would be the output filename 

        Example - Structure will be like this: 

        Year | Pokemon Cards Released | Pokemon Sets Released | Yu-Gi-Oh Cards Released | Yu-Gi-Oh Sets Released |
        1999 |          500          |          5           |          300           |          3            |

    """

    with open(filename, 'w') as f:

        all_years = set(pokemon_total_cards.keys()) | set(pokemon_sets.keys()) | set(yugioh_total_cards.keys()) | set(yugioh_sets.keys())
        sorted_years = sorted(list(all_years))

        f.write("Combined Pokemon & Yu-Gi-Oh Calculation Results:\n")
        f.write('\n')
        f.write("-" * 80 + '\n')
        f.write('\n')

        # columns width for formatting 

        column_widths = 15
        year_widths = 6 

        # header 

        header = f'{"Year":<{year_widths}} | {"Pokemon Cards Released":<{column_widths}} | {"Pokemon Sets Released":<{column_widths}} | {"Yu-Gi-Oh Cards Released":<{column_widths}} | {"Yu-Gi-Oh Sets Released":<{column_widths}} |'
        f.write(header + "\n")
        f.write("-" * 80 + "\n")


        for year in sorted_years:
            pokemon_total_cards = pokemon_total_cards.get(year, 0)
            pokemon_sets = pokemon_sets.get(year, 0)
            yugioh_total_cards = yugioh_total_cards.get(year, 0)
            yugioh_sets = yugioh_sets.get(year, 0)


            # Each of the rows 

            row = f'{year:<{year_widths}} | {pokemon_total_cards:<{column_widths}} | {pokemon_sets:<{column_widths}} | {yugioh_total_cards:<{column_widths}} | {yugioh_sets:<{column_widths}} |'
            f.write(row + "\n")
       
    pass



        # f.write("-" * 30 + "\n\n")
        # f.write("Pokemon Calculation Results:\n\n")
        # f.write("-" * 30 + "\n\n")

        # f.write("Pokemon Cards Released Per Year:\n\n")
        # f.write("-" * 30 + "\n\n")

        # for year in sorted(pokemon_total_cards.keys()):
        #     f.write(f'{year}: {pokemon_total_cards[year]}\n')
        # f.write('\n')

        # f.write("-" * 30 + "\n\n")
        # f.write("Pokemon Sets Released Per Year:\n")
        # f.write("-" * 30 + "\n\n")

        # for year in sorted(pokemon_sets.keys()):
        #     f.write(f'{year}: {pokemon_sets[year]}\n')

        # f.write('\n' + "-" * 30 + '\n\n')
        # f.write("Yu-Gi-Oh Calculation Results:\n")
        # f.write('\n' + "-" * 30 + '\n\n')

        # f.write("Yu-Gi-Oh Cards Released Per Year:\n")
        # f.write("-" * 30 + "\n")

        # for year in sorted(yugioh_total_cards.keys()):
        #     f.write(f'{year}: {yugioh_total_cards[year]}\n')
        # f.write('\n')

        # f.write("Yu-Gi-Oh Sets Released Per Year:\n")
        # f.write("-" * 30 + "\n")

        # for year in sorted(yugioh_sets.keys()):
        #     f.write(f'{year}: {yugioh_sets[year]}\n')

    print(f"Yu-Gi-Oh & PokemonCalculation results written to {filename}")

def main():
    # Look back on Discussion for to have the full path to the database file.

    conn = sqlite3.connect('tcg_data.db')

    pokemon_total_per_year = calculate_pokemon_total_per_year(conn)
    create_pokemon_histogram(pokemon_total_per_year, "Total Pokemon Cards Released Per Year", "Year", "Total Cards Released Per Year")
    pokemon_sets_per_year = calculate_pokemon_sets_per_year(conn)
    create_pokemon_histogram(pokemon_sets_per_year, "Total Pokemon Sets Released Per Year", "Year", "Total Sets Released")

    yugioh_total_per_year = calculate_yugioh_total_per_year(conn)
    create_yugioh_histogram(yugioh_total_per_year, "Total Yu-Gi-Oh Cards Released Per Year", "Year", "Total Cards Released")
    yugioh_sets_per_year = calculate_yugioh_sets_per_year(conn)
    create_yugioh_histogram(yugioh_sets_per_year, "Total Yu-Gi-Oh Sets Released Per Year", "Year", "Total Sets Released")
    
    write_calculation_to_file(pokemon_total_per_year, pokemon_sets_per_year, yugioh_total_per_year, yugioh_sets_per_year)
    
    conn.close()

if __name__ == "__main__":
    main()