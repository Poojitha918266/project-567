import sqlite3

def recommend_recipes(user_id, available_ingredients):
    # Connect to the SQLite database
    conn = sqlite3.connect('recipe_recommendation.db')
    cursor = conn.cursor()

    # Get the user's dietary restriction
    cursor.execute('SELECT dietary_restriction FROM users WHERE user_id = ?', (user_id,))
    dietary_restriction = cursor.fetchone()[0]

    # Build a query to find recipes that can be made with available ingredients
    query = '''
    SELECT r.recipe_name, r.instructions
    FROM recipes r
    JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
    JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    WHERE i.ingredient_name IN ({})
    GROUP BY r.recipe_id
    HAVING COUNT(ri.ingredient_id) = ?
    '''.format(','.join('?' * len(available_ingredients)))

    # Execute the query
    cursor.execute(query, available_ingredients + [len(available_ingredients)])
    recommendations = cursor.fetchall()

    # Close the connection
    conn.close()
    return recommendations

# Example usage
user_id = 1  # assuming user_id 1 is a vegetarian
available_ingredients = ['Tomato', 'Pasta']  # ingredients the user has
recommended_recipes = recommend_recipes(user_id, available_ingredients)

print("Recommended Recipes:")
for recipe in recommended_recipes:
    print(f"Recipe: {recipe[0]}, Instructions: {recipe[1]}")
