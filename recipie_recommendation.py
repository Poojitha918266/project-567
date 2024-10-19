import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('recipe_recommendation.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS recipe_ingredients")
cursor.execute("DROP TABLE IF EXISTS recipes")
cursor.execute("DROP TABLE IF EXISTS ingredients")
cursor.execute("DROP TABLE IF EXISTS users")

# Create tables
cursor.execute('''
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        dietary_preference TEXT,
        favorite_cuisine TEXT
    )
''')

cursor.execute('''
    CREATE TABLE ingredients (
        ingredient_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE recipes (
        recipe_id INTEGER PRIMARY KEY,
        name TEXT,
        prep_time INTEGER,
        instructions TEXT
    )
''')

cursor.execute('''
    CREATE TABLE recipe_ingredients (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id)
    )
''')

# Sample data
users = [(1, 'vegetarian', 'Italian'), (2, 'none', 'Mexican')]
ingredients = [(1, 'Tomato'), (2, 'Pasta'), (3, 'Cheese'), (4, 'Beans')]
recipes = [
    (1, 'Pasta Primavera', 20, 'Cook pasta and add vegetables.'),
    (2, 'Caprese Salad', 10, 'Layer tomato and mozzarella with basil.'),
    (3, 'Bean Tacos', 15, 'Fill tortillas with beans and toppings.')
]

# Insert data into tables
cursor.executemany('INSERT INTO users VALUES (?, ?, ?)', users)
cursor.executemany('INSERT INTO ingredients VALUES (?, ?)', ingredients)
cursor.executemany('INSERT INTO recipes VALUES (?, ?, ?, ?)', recipes)

# Link recipes to ingredients
recipe_ingredients = [(1, 1), (1, 2), (2, 1), (2, 3), (3, 4)]
cursor.executemany('INSERT INTO recipe_ingredients VALUES (?, ?)', recipe_ingredients)

# Commit changes
conn.commit()

# Function to check the structure of the recipes table
def check_recipes_table():
    cursor.execute("PRAGMA table_info(recipes)")
    columns = cursor.fetchall()
    print("Columns in 'recipes' table:")
    for column in columns:
        print(column)

# Function to recommend recipes based on dietary preference
def recommend_vegetarian_recipes(user_id):
    cursor.execute('''
        SELECT DISTINCT r.name, r.instructions
        FROM recipes r
        JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN users u ON u.user_id = ?
        WHERE u.dietary_preference = 'vegetarian'
    ''', (user_id,))
    
    recommended_recipes = cursor.fetchall()
    
    if recommended_recipes:
        for recipe in recommended_recipes:
            print(f"Recipe: {recipe[0]}, Instructions: {recipe[1]}")
    else:
        print("No vegetarian recipes found for this user.")

# Check the structure of the recipes table
check_recipes_table()

# Run the recommendation query for vegetarian recipes for user_id = 1
recommend_vegetarian_recipes(1)

# Close the connection
conn.close()
