#DOUBLE CHECK THIS FILE TASK IS FOR YOU "CALCULATION"



def calculate_yugioh_creatures_per_year(conn):
    """
    Calculate the number of unique Yu-Gi-Oh! creature cards released each year
    
    Args:
        conn: SQLite database connection
        
    Returns:
        dict: {year: count} - Number of creature cards per year
    """
    cursor = conn.cursor()
    
    # How to get monster cards (Type = 'Monster') with tcg_data (place holder)  
    cursor.execute("""
        SELECT tcg_data, COUNT(DISTINCT card_id) 
        FROM yugioh_cards 
        WHERE Type = 'Monster'
        GROUP BY tcg_data
    """)
    
    results = cursor.fetchall()
    
    # Get the results into the year-based dictionary
    year_counts = defaultdict(int)
    for date_str, count in results:
        if date_str:
            year = date_str.split('-')[0]
            year_counts[year] += count
    
    return dict(year_counts)


# Brandon