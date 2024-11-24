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

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

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

def create_recipe(conn, cursor):

    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients of the recipe: ")

  

    difficulty = calc_difficulty(cooking_time, ingredients)

    ingredients_str = ", ".join(ingredients)

    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'

    values = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, values)
    conn.commit()
    print("Recipe has been successfully added to the database!")

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

def search_recipe(conn, cursor):
    cursor.execute('SELECT DISTINCT ingredients FROM Recipes')
    results = cursor.fetchall()

    # Extract ingredients from the fetched results
    all_ingredients = []
    for row in results:
        ingredient = row[0]
        ingredients_list = ingredient.split(", ")
        all_ingredients.extend(ingredients_list)

    # Remove duplicates and sort the ingredients list
    all_ingredients = sorted(set(all_ingredients))

    # Display all ingredients to the user
    print("Available ingredients:")
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}. {ingredient}")

    ing_index = int(input("Enter the number corresponding to the ingredient you want to search for: "))
    search_ingredient = all_ingredients[ing_index -1]

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



def update_recipe(conn, cursor):
    cursor.execute('SELECT id, name FROM Recipes')
    recipes = cursor.fetchall()

    print("Available Recipes: ")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    update_column = input("Enter the column to update (name, ingredients, cooking_time): ")

    new_value = input("Enter the new value: ")

    if update_column == 'name':
        cursor.execute('UPDATE Recipes SET name = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

    elif update_column == 'ingredients':
        cursor.execute('UPDATE Recipes SET ingredients = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

    elif update_column == 'cooking_time':
        cursor.execute('UPDATE Recipes SET cooking_time = %s WHERE %s', (new_value, recipe_id))
        print(update_column, "has been updated!")

    else:
        print("Invalid Column")
        return
    
    if update_column in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        difficulty = calc_difficulty(row[0], row[1])
        update_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(update_query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully!")

def delete_recipe(conn, cursor):
    cursor.execute('SELECT id, name FROM Recipes')
    results = cursor.fetchall()

    print("\nExisiting Recipes: ")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))

    conn.commit()
    print("Recipe deleted successfully!")


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
    