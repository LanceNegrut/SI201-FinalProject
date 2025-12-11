# Brandon Reyes Parra


import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt 
import numpy as np


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

    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color="skyblue", edgecolor="black", linewidth=1.5)
    #plt.bar(years, counts)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', alpha=0.75, linestyle='--')
    plt.tight_layout()
    plt.show()

def calculate_yugioh_total_per_year(conn):

    """
    Calculate the total number of cards of all Yu-Gi-Oh creature cards released each year
    
    Args:
        conn: SQLite database connection
    Returns: 
        dict: {year: total_cards} - total cards released per year
    """
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT rd.tcg_date, SUM(ps.num_of_cards)
        FROM "Yu-Gi-Oh Release Dates" rd
        JOIN "Yu-Gi-Oh Sets" ps ON rd.tcg_date_id = ps.tcg_date_id
        GROUP BY rd.tcg_date
    """)
    
    results = cursor.fetchall()
    
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


    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color="lightcoral", edgecolor="black", linewidth=1.5)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', alpha=0.75, linestyle='--')
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


    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)
    x = np.arange(len(all_years))
    width = 0.25

    bars1 = ax.bar(x - width, pokemon_values, width, label='Pokemon', color='skyblue', edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x, yugioh_values, width, label='Yu-Gi-Oh', color='lightcoral', edgecolor='black', linewidth=1.5)

    ax.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax.set_ylabel('Total Cards Released', fontsize=13, fontweight='bold')
    ax.set_title('TCG Production Trends: Pokemon vs Yu-Gi-Oh Over the Years', fontsize=16, fontweight='bold')
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.7, zorder=0)

    ax.set_xticks(x)
    ax.set_xticklabels(all_years, rotation=45, ha='right')
    ax.legend(loc='best')

    plt.tight_layout()
    plt.show()


def calculate_average_cards_per_set(conn):
    """
    We are going to get the avarege cards per set for each year.
    SHow the trend: Sets getting bigger or smaller over time.

    Returns:
    tuple: (pokemon_avg_per_set, yugioh_avg_per_set)

    """

    pokemon_cards = calculate_pokemon_total_per_year(conn)
    pokemon_sets = calculate_pokemon_sets_per_year(conn)
    yugioh_cards = calculate_yugioh_total_per_year(conn)
    yugioh_sets = calculate_yugioh_sets_per_year(conn)

    pokemon_average = {}
    for year in pokemon_cards.keys():
        if year in pokemon_sets and pokemon_sets[year] > 0:
            pokemon_average[year] = round(pokemon_cards[year] / pokemon_sets[year], 1)

    yugioh_average = {}
    for year in yugioh_cards.keys():
        if year in yugioh_sets and yugioh_sets[year] > 0:
            yugioh_average[year] = round(yugioh_cards[year] / yugioh_sets[year], 1)
    
    return pokemon_average, yugioh_average

def create_average_sets_line_chart(pokemon_average, yugioh_average):
    """
    Line Chart: This would show the the average set size trends. 

    Args:
        pokemon_average: average cards per set for Pokemon
        yugioh_average: average cards per set for Yu-Gi-Oh

    """

    all_years = sorted(set(pokemon_average.keys()) | set (yugioh_average.keys()))
    pokemon_values = [pokemon_average.get(year, 0) for year in all_years]
    yugioh_values = [yugioh_average.get(year, 0) for year in all_years]

    plt.figure(figsize=(10, 6))
    
    plt.plot(all_years, pokemon_values, marker='o', linewidth=2, markersize=6, label='Pokemon Avg Set Size', color='skyblue', linestyle='-') # pokemon line
        
    plt.plot(all_years, yugioh_values, marker='s', linewidth=2, markersize=6, label='Yu-Gi-Oh Avg Set Size', color='lightcoral', linestyle='-') # yugioh line


    plt.xlabel('Year', fontsize=13, fontweight='bold')
    plt.ylabel('Avg Cards Per Set', fontsize=13, fontweight='bold')
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def write_calculation_to_file(conn, pokemon_total_cards, pokemon_sets, yugioh_total_cards, yugioh_sets, filename='All_calculation.txt'):

    """
    Write calculated on result to a text file with both Pokemon and Yu-Gi-Oh data

    Args:
        total_cards_data: dict of the total cards released per year 
        sets_data: dict of the total sets released per year 
        filename: this would be the output filename 

        Example - Structure will be like this: 

        Year | Pokemon Cards Released | Pokemon Sets Released | Yu-Gi-Oh Cards Released | Yu-Gi-Oh Sets Released |
        1999 |          500          |          5           |          300           |          3            |

    
    #I'm doing an Update here to have similar structure but adding more to it.
    """

    pokemon_average, yugioh_average = calculate_average_cards_per_set(conn)

    with open(filename, 'w') as f:
        all_years = set(pokemon_total_cards.keys()) | set(pokemon_sets.keys()) | set(yugioh_total_cards.keys()) | set(yugioh_sets.keys()) 
        sorted_years = sorted(list(all_years))

        f.write("Section 1:Pokemon & Yu-Gi-Oh Calculation Results:\n")
        f.write("Functions Generated Table: calculating total cards and sets released per year\n")
        f.write("=" * 100 + "\n")

        column_widths = 12
        year_widths = 6

        header = f'{"Year":<{year_widths}} | {"Pokemon Cards":<{column_widths}} | {"Pokemon Sets":>{column_widths}} | {"Yu-Gi-Oh Cards":<{column_widths}} | {"Yu-Gi-Oh Sets":<{column_widths}}'
        f.write(header + "\n")
        f.write("=" * 100 + "\n")

        for year in sorted_years:
            poke_cards_total = pokemon_total_cards.get(year, 0)
            poke_sets_total = pokemon_sets.get(year, 0)
            yugioh_cards_total = yugioh_total_cards.get(year, 0)
            yugioh_sets_total = yugioh_sets.get(year, 0)
        
            row = f'{year:<{year_widths}} | {poke_cards_total:<{column_widths}} | {poke_sets_total:<{column_widths}} | {yugioh_cards_total:<{column_widths}} | {yugioh_sets_total:<{column_widths}}'
            f.write(row + "\n")

        f.write("=" * 100 + "\n")
        f.write("Section 2: Average cards per set for all years:\n")
        f.write("=" * 100 + "\n")

        header_two = f'{"Year":<{year_widths}} | {"Pokemon Avg":<{column_widths}} | {"Yu-Gi-Oh Avg":<{column_widths}}'
        f.write(header_two + "\n")
        f.write("=" * 100 + "\n")
        for year in sorted_years:
            pokemon_avg = pokemon_average.get(year, 0)
            yugioh_avg = yugioh_average.get(year, 0)
            row_two = f'{year:<{year_widths}} | {pokemon_avg:<{column_widths}} | {yugioh_avg:<{column_widths}}'
            f.write(row_two + "\n")

        poke_years_sorted = sorted(pokemon_average.keys())
        yugio_years_sorted = sorted(yugioh_average.keys())

        early_years_poke = poke_years_sorted[:5]
        early_years_yugio = yugio_years_sorted[:5]
        recent_years_poke = poke_years_sorted[-5:]
        recent_years_yugio = yugio_years_sorted[-5:]

        f.write("=" * 100 + "\n")
        f.write("Section 3: Growth Analysis:\n")

        if early_years_poke and recent_years_poke and early_years_yugio and recent_years_yugio:
            
            pokemon_early_avg = sum(pokemon_average[year] for year in early_years_poke) / len(early_years_poke)
            pokemon_recent_avg = sum(pokemon_average[year] for year in recent_years_poke) / len(recent_years_poke)
            yugioh_early_avg = sum(yugioh_average[year] for year in early_years_yugio) / len(early_years_yugio)
            yugioh_recent_avg = sum(yugioh_average[year] for year in recent_years_yugio) / len(recent_years_yugio)
        f.write("=" * 100 + "\n")
        if pokemon_early_avg > 0:
            if pokemon_recent_avg > pokemon_early_avg:
                pokemon_growth = ((pokemon_recent_avg - pokemon_early_avg) / pokemon_early_avg) * 100 
                f.write(f"Pokemon sets grew by {pokemon_growth:.1f}% (from {pokemon_early_avg:.1f} to {pokemon_recent_avg:.1f} cards per set)\n")
            else:
                pokemon_recent_decline = ((pokemon_early_avg - pokemon_recent_avg) / pokemon_early_avg) * 100
                f.write(f"Pokemon sets declined by {pokemon_recent_decline:.1f}% (from {pokemon_early_avg:.1f} to {pokemon_recent_avg:.1f} cards per set)\n")
            if yugioh_early_avg > 0:
                if yugioh_recent_avg > yugioh_early_avg:
                    yugioh_growth = ((yugioh_recent_avg - yugioh_early_avg) / yugioh_early_avg) * 100
                    f.write(f"Yu-Gi-Oh sets grew by {yugioh_growth:.1f}% (from {yugioh_early_avg:.1f} to {yugioh_recent_avg:.1f} cards per set)\n")
                else:
                    yugioh_decline = ((yugioh_early_avg - yugioh_recent_avg) / yugioh_early_avg) * 100
                    f.write(f"Yu-Gi-Oh sets declined by {yugioh_decline:.1f}% (from {yugioh_early_avg:.1f} to {yugioh_recent_avg:.1f} cards/set\n")
        f.write("=" * 100 + "\n")
    conn.close()
    print(f"Calculation results written to a {filename}")

def main():
    conn = sqlite3.connect('tcg_data.db')

    # Calculate individual card
    pokemon_total_per_year = calculate_pokemon_total_per_year(conn)
    create_pokemon_histogram(pokemon_total_per_year, "Total Pokemon Cards Released Per Year", "Year", "Total Cards Released")
    pokemon_sets_per_year = calculate_pokemon_sets_per_year(conn)
    create_pokemon_histogram(pokemon_sets_per_year, "Total Pokemon Sets Released Per Year", "Year", "Total Sets Released Per Year")
    print(f"Pokemon {sum(pokemon_total_per_year.values())} cards, {sum(pokemon_sets_per_year.values())} sets")

    yugioh_total_per_year = calculate_yugioh_total_per_year(conn)
    create_yugioh_histogram(yugioh_total_per_year, "Total Yu-Gi-Oh Cards Released Per Year", "Year", "Total Cards Released")
    yugioh_sets_per_year = calculate_yugioh_sets_per_year(conn)
    create_yugioh_histogram(yugioh_sets_per_year, "Total Yu-Gi-Oh Sets Released Per Year", "Year", "Total Sets Released Per Year")
    print(f"Yu-Gi-Oh {sum(yugioh_total_per_year.values())} cards, {sum(yugioh_sets_per_year.values())} sets")
    
    # Now here we do a JOIN calculation.
    combined_data, pokemon_data, yugioh_data = joining_tables(conn) 
    create_combined_histogram(pokemon_data, yugioh_data, combined_data)

    # Next will be the Avg.
    pokemon_average, yugioh_average = calculate_average_cards_per_set(conn)
    create_average_sets_line_chart(pokemon_average, yugioh_average)

    write_calculation_to_file(conn, pokemon_total_per_year, pokemon_sets_per_year, yugioh_total_per_year, yugioh_sets_per_year)
    # write_calculation_to_file(pokemon_total_per_year, pokemon_sets_per_year, yugioh_total_per_year, yugioh_sets_per_year)
    conn.close()

if __name__ == "__main__":
    main()