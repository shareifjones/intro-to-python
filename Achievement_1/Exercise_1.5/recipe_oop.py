class Recipe(object):
        def __init__(self, name):
            self.name = name
            self.ingredients = []
            self.cooking_time = int
            self.difficulty = None

# Gets recipe name
        def get_name(self):
            return self.name
        
# Sets recipe name
        def set_name(self, name):
            self.name = name



# Gets recipe cooking time
        def get_cooking_time(self):
            return self.cooking_time

 # Sets recipe cooking time        
        def set_cooking_time(self, cooking_time):
            self.cooking_time = cooking_time



# Sets a class variable to store all ingredients across all recipes
        all_ingredients = set()

# Gets the ingredients list
        def get_ingredients(self):
            return self.ingredients

# Adds ingredients to a recipe
        def add_ingredients(self, *ingredients):
            for ingredient in ingredients:
                self.ingredients.append(ingredient)

# Updates list of all ingredients
            self.update_all_ingredients()

 # Searches for an ingredient
        def search_ingredient(self, ingredient):
            return ingredient in self.ingredients
        
 # Updates the list of all ingredients when a new one is added        
        def update_all_ingredients(self):
            for ingredient in self.ingredients:
                Recipe.all_ingredients.add(ingredient)




 # Determines recipe difficulty
        def calc_difficulty(self):
            if self.cooking_time < 10 and len(self.ingredients) < 4:
                self.difficulty = "Easy"
            elif self.cooking_time < 10 and len(self.ingredients) >= 4:
                self.difficulty = "Medium"
            elif self.cooking_time >= 10 and len(self.ingredients) < 4:
                self.difficulty = "Intermediate"
            elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
                self.difficulty = "Hard"

# Gets a recipe's difficulty        
        def get_difficulty(self):
            if not self.difficulty:
                self.calc_difficulty()
            return self.difficulty

        def __str__(self):
            return f"Recipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time (minutes): {self.cooking_time}\nDifficulty: {self.get_difficulty()}\n"

# Searches for recipes containing a specified ingredient        
def recipe_search(data, ingredient):
    for recipe in data:
        if recipe.search_ingredient(ingredient):
            print(recipe)


# Initializes object "Tea"
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)
# Initializes object "Coffee"
coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee)
# Initializes object "Cake"
cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
print(cake)
# Initializes object "Banana Smoothie"
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
print(banana_smoothie)

# Initializes list "Recipes List"
recipes_list = [tea, coffee, cake, banana_smoothie]


# Uses recipe_search() to find ingredients in recipes_list
print("\nRecipes with water: ")
recipe_search(recipes_list, "Water")

print("\nRecipes with sugar: ")
recipe_search(recipes_list, "Sugar")

print("\nRecipes with bananas: ")
recipe_search(recipes_list, "Bananas")