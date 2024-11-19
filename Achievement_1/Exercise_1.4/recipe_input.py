recipes_list = []
all_ingredients = []


import pickle

# Function to take user input for recipe components
def take_recipe():
    name = str(input("Enter the recipe's name: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients: ").split(", "))

    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    
    return recipe
   

    # Iterates through recipes_list to determine recipe difficulty
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    if cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    if cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    if cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"

    return difficulty

    
    
# Has the user enter a file name to search
file_name = input("Please enter the file name: ")

# Trys to open the searched file but if it doesnt exists, creates a file
try:
    file = open(file_name, "rb")
    data = pickle.load(recipes_list, all_ingredients)

# This is the error that will be raised if the file doesn't exist
except FileNotFoundError:
    print("This file was not found. A new one will be created.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

# This error is for all other errors
except:
    print("We've ran into an unexpected problem")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

# This closes the file
else:
    file.close()

# extracts the values from the dictionary into two separate lists
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]


n = int(input("How many recipes will you like to enter?"))

# Iterates through number of given recipes
for i in range(n):
    recipe = take_recipe()

# Checks whether an ingredient should be added to an ingredient list
    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)
    print("Your recipe has been added!")

# Gathering all attributes into a dictionary and returning it.
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}


# Opens the file and saves the data to it
updated_file = open(file_name, 'wb')
pickle.dump(data, updated_file)
updated_file.close()
print("File updated.")