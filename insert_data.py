import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('recipe_recommendation.db')
cursor = conn.cursor()

# Create tables if they don't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    dietary_preference TEXT,
    favorite_cuisine TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY,
    name TEXT,
    prep_time INTEGER,
    instructions TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
)''')

# Sample data
users = [(1, 'vegetarian', 'Italian'), (2, 'none', 'Mexican')]
ingredients = [(1, 'Tomato'), (2, 'Pasta'), (3, 'Cheese'), (4, 'Beans')]
recipes = [
    (1, 'Pasta Primavera', 20, 'Cook pasta and add vegetables.'),
    (2, 'Caprese Salad', 10, 'Layer tomato and mozzarella with basil.'),
    (3, 'Bean Tacos', 15, 'Fill tortillas with beans and toppings.')
]

# Insert data into tables using INSERT OR IGNORE to avoid conflicts
cursor.executemany('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', users)
cursor.executemany('INSERT OR IGNORE INTO ingredients VALUES (?, ?)', ingredients)
cursor.executemany('INSERT OR IGNORE INTO recipes VALUES (?, ?, ?, ?)', recipes)

# Link recipes to ingredients
recipe_ingredients = [(1, 1), (1, 2), (2, 1), (2, 3), (3, 4)]
cursor.executemany('INSERT OR IGNORE INTO recipe_ingredients VALUES (?, ?)', recipe_ingredients)

# Commit changes and close the connection
conn.commit()
conn.close()
