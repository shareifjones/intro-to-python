from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_database")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
    
    def __str__(self):
        return (f"Recipe ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Ingredients: {self.ingredients}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Diffculty: {self.difficulty}"
                )


    def calc_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"
        else:
            print("An error has occurred. Please try again!")

        print("Difficulty level: ", self.difficulty)
        return self.difficulty
    
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(", ")
    
Base.metadata.create_all(engine)

def name_input():
    name = input("Please enter the name of the recipe (max 50 characters): ")
    while len(name) > 50:
        name = input("Recipe name is too long.  Please enter again (max 50 characters): ")
    return name

def ingredients_input():
    while True:
        try:
            num_ingredients = int(input("How many ingredients? "))
            if num_ingredients <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    ingredients = []
    for _ in range(num_ingredients):
        ingredient = input("Please enter the ingredients one by one: ")
        if any(char.isalpha() for char in ingredient) and not ingredient.isnumeric():
                    ingredients.append(ingredient)
                    
        else:
                    print("Invalid ingredient. It should not be purely numeric and must contain at least one letter. Please try again.")
    return ', '.join(ingredients)

def cooking_time_input():
    cooking_time = input("Please enter the cooking time in minutes: ")
    while not cooking_time.isnumeric():
          cooking_time = input("Invalid response.  Please only enter numbers: ")
    return int(cooking_time)

def create_recipe():
     name = name_input()
     ingredients = ingredients_input()
     cooking_time = cooking_time_input()

     recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
     recipe_entry.difficulty = recipe_entry.calc_difficulty()

     session.add(recipe_entry)
     session.commit()
     print("Recipe successfully added!")

def view_all_recipes():
     recipes = session.query(Recipe).all()
     if len(recipes) == 0:
          print("No recipes found.")
     else:
        print("\nHere is the list of recipes: ")

     for recipe in recipes:
        print(recipe)


def search_by_ingredients():
    check_ingredients = session.query(Recipe).all()
    if len(check_ingredients) == 0:
        print("There are no ingredients in the database.")
        return
    else:
        results = session.query(Recipe.ingredients).all()

    # Extract unique ingredients
    all_ingredients = []
    for result in results:
        ingredients_list = result[0].split(', ')
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display available ingredients
    print("Available ingredients:")
    ingredient_dict = {str(index): ingredient for index, ingredient in enumerate(all_ingredients, start=1)}
    for index, ingredient in ingredient_dict.items():
        print(f"{index}. {ingredient}")

    # Get user input and validate
    ing_indexes = input("Enter the numbers of the ingredients you'd like to search for (separated by spaces): ").split()
    try:
        search_ingredients = [ingredient_dict[index] for index in ing_indexes]
    except KeyError:
        print("Invalid input. Please enter valid ingredient numbers.")
        return

    # Search recipes containing all selected ingredients
    search_results = session.query(Recipe).filter(
        *[Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    ).all()

    # Display search results
    print("\nSearch Results:")
    if search_results:
        for result in search_results:
            print(f"Name: {result.name}")
            print(f"Ingredients: {result.ingredients}")
            print(f"Cooking Time: {result.cooking_time} minutes")
            print(f"Difficulty: {result.difficulty}\n")
    else:
        print(f"No recipes found with {', '.join(search_ingredients)}.")


def edit_recipe():
    check_recipes = session.query(Recipe).count()
    if check_recipes == 0:
          print("There are no recipes in the database.")
          return None
     
    results = session.query(Recipe.id, Recipe.name).all()

    for result in results:
          print(f"ID: {result.id}, Name: {result.name}")

    pick_id = input("Please choose a recipe by ID number: ")
    recipe_to_edit = session.query(Recipe).filter_by(id=pick_id).first()
    if not recipe_to_edit:
          print("Recipe was not found.")
          return None
     
    print (recipe_to_edit)

    attribute = input("Please enter the number of the attribute you'd like to edit! Name: 1, Ingredients: 2, Cooking Time: 3: \n")

    if attribute == '1':
        recipe_to_edit.name = name_input()
    elif attribute == '2':
        recipe_to_edit.ingredients = ingredients_input()
    elif attribute == '3':
        recipe_to_edit.cooking_time = cooking_time_input()
    else:
         print("Invalid choice")
         return None   
    
    recipe_to_edit.difficulty = recipe_to_edit.calc_difficulty()
    session.commit()
    print("Reciped successfully edited!")

def delete_recipe():
    check_recipes = session.query(Recipe).count()
    if check_recipes == 0:
          print("There are no recipes in the database.")
          return None
    
    results = session.query(Recipe.id, Recipe.name).all()

    for result in results:
          print(f"ID: {result.id}, Name: {result.name}")

    id_to_delete = input("Enter the ID number of the recipe you'd like to delete: ")
    recipe_to_delete = session.query(Recipe).filter_by(id=id_to_delete).first()
    if not recipe_to_delete:
         ("Recipe was not found")
         return None
    
    confirmation = input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ").strip().lower()
    if confirmation.lower() == 'yes':
         session.delete(recipe_to_delete)
         session.commit()
         print("Recipe successfully deleted!")

    else:
         print("Deletion cancelled")
         return None
    
def main_menu():
     while True:
        print("\nMain Menu")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5: View all recipes")
        print("6. Quit")
    
        choice = input("Enter the number your choice: ")

        if choice == '1':
            create_recipe()
        elif choice == '2':
            search_by_ingredients()
        elif choice == '3':
            edit_recipe()
        elif choice == '4':
            delete_recipe()
        elif choice == '5':
            view_all_recipes()
        elif choice == '6':
            print("Quitting program...")
            break
        else:
            print("Invalid choice. Please try again.")

     session.close()
     engine.dispose()

main_menu()



    
     
          
    
    
         
    
    
     

