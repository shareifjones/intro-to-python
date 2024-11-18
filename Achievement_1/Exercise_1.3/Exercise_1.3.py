recipes_list = []
ingredients_list = []


# Function to take user input for recipe components
def take_recipe():
    name = str(input("Enter the recipe's name: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    
    return recipe

n = int(input("How many recipes will you like to enter?"))

# Iterates through number of given recipes
for i in range(n):
    recipe = take_recipe()

# Checks whether an ingredient should be added to an ingredient list
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

# Iterates through recipes_list to determine recipe difficulty
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"

    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficutly"] = "Medium"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

# Iterates through recipes_list to display info
for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking Time (min): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# Displays all of the ingredients from all recipes in alphabetical order
def all_ingredients():
    print("Ingredients Available Across All Recipes: ")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()