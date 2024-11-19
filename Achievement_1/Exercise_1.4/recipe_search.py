import pickle

# Displays all data related to a recipe
def display_recipe(recipe):
    print("Recipe: ", recipe["name"])
    print("Cooking Time (min): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# Function that searches through the ingredients
def search_ingredient(data):
    # Adds a number to the ingredients
    all_ingredients = enumerate(data["all_ingredients"])
    #Puts the numbered data into a list
    number_ingredients = list(all_ingredients)

    for ingredient in number_ingredients:
        print(ingredient[0], ingredient[1])


    try:
        n = int(input("Enter the number of an ingredient to search: "))
        # Searches for number associated with ingredient
        ingredient_searched = number_ingredients[n][1]
        print("Searching for recipes including", ingredient_searched, "...")

    except ValueError:
        print("Only numbers are allowed")

    except:
        print("Your input does not match any ingredient stored.")
    
    else:
        # Goes through each recipe and displays the ones with the ingredient
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

filename = input("Please enter the file name: ")

try:
    file = open(filename, 'rb')
    data = pickle.load(file)
    print("File loaded successfully!")

except FileNotFoundError:
    print("The file has not been found.")

else:
    # Closes file stream and initializes search_ingredient()
    file.close()
    search_ingredient(data)


  
    