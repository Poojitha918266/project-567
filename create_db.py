import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('recipe_recommendation.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    dietary_restriction TEXT,
    favorite_cuisine TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    ingredient_name TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER PRIMARY KEY,
    recipe_name TEXT,
    cooking_time INTEGER,  -- in minutes
    instructions TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
)''')

# Commit changes and close the connection
conn.commit()
conn.close()
