# steps to connect mysql
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
    )

if conn.is_connected():
    print("Connection successful!")
else:
    print("Connection failed!")

cursor = conn.cursor()

# creates a data base named task_database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# selects the database to use
cursor.execute("USE task_database")

# creates a table called Recipes with the following columns
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS recipes (
        id INT NOT NULL  PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    '''
)

# creates a recipe using the different columns, then adds the recipes to the database
def create_recipe(conn, cursor):

    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients of the recipe: ")
    difficulty = calc_difficulty(cooking_time, ingredients)

# adds recipes to table
    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    values = (name, ingredients, cooking_time, difficulty)

    cursor.execute(sql, values)
    conn.commit()
    print("Recipe has been successfully added to the database!")

# calculates the difficulty of a recipe based on time and length of ingredients
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    else:
        print("An error has occurred. Please try again!")

    print("Difficulty level: ", difficulty)
    return difficulty

# allows to search for a recipe based on ingredients
def search_recipe(conn, cursor):
    # chooses the ingredients column to search from
    cursor.execute('SELECT DISTINCT ingredients FROM Recipes')
    results = cursor.fetchall()

    # Extract ingredients from the fetched results
    all_ingredients = []
    for row in results:
        ingredient = row[0]
        ingredients_list = ingredient.split(",")
        all_ingredients.extend(ingredients_list)

    # Remove duplicates and sort the ingredients list
    all_ingredients = sorted(set(all_ingredients))

    # Displays all ingredients to the user
    print("Available ingredients:")
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}. {ingredient}")

    ing_index = int(input("Enter the number corresponding to the ingredient you want to search for: "))
    search_ingredient = all_ingredients[ing_index -1]

# grabs all recipes that have the selected ingredient
    sql = 'SELECT * FROM Recipes WHERE ingredients LIKE %s'

    cursor.execute(sql, ('%' + search_ingredient + '%',))
    results = cursor.fetchall()

    print("Search Results: ")
    for row in results:
        print("\nID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3], "minutes")
        print("Difficulty: ", row[4])

    # else:
    #     print("There are no recipes containing: ", search_ingredient)


# updates a recipe based on the recipes ID number
def update_recipe(conn, cursor):
    cursor.execute('SELECT id, name FROM Recipes')
    recipes = cursor.fetchall()

# shows the entire list of recipes in the database
    print("Available Recipes: ")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    update_column = input("Enter the column to update (name, ingredients, cooking_time): ")

    new_value = input("Enter the new value: ")

# name will allow the user to set a new name that matches the id they've chosen
    if update_column == 'name':
        cursor.execute('UPDATE Recipes SET name = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

# ingredients will allow the user to update the ingredients to a recipe
    elif update_column == 'ingredients':
        cursor.execute('UPDATE Recipes SET ingredients = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

# cooking time will allow the user to set a new cooking time and update the difficulty that matches the id they've chosen
    elif update_column == 'cooking_time':
        cursor.execute('UPDATE Recipes SET cooking_time = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

    else:
        print("Invalid Column")
        return

# this recalcuates the difficulty if the user updates either the ingredients and/or cooking time
    if update_column in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        difficulty = calc_difficulty(row[0], row[1])
        update_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(update_query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully!")

# this deletes a recipe based on ID number
def delete_recipe(conn, cursor):
    cursor.execute('SELECT id, name FROM Recipes')
    results = cursor.fetchall()

# this displays all recipes in the database
    print("\nExisiting Recipes: ")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))

    conn.commit()
    print("Recipe deleted successfully!")

# the main menu that the user starts off seeing and allows them to choose
def main_menu(conn, cursor):
    while True:
        print("\nMain Menu")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Quit")
    
        choice = input("Enter your choice: ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Quitting program...")
            break
        else:
            print("Invalid choice. Please try again.")
        
         # Commit changes and close connection before exiting
    conn.commit()
    conn.close()
    print("Database connection closed.")

# Call the main_menu function
main_menu(conn, cursor)
    