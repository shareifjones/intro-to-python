# Defines ShoppingList class
class ShoppingList(object):
    # Initializes data attributes
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

# Defines function to add an item to the list if not already present
    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)
            print("Item added to shopping list.")
        else:
            print("Item already in shopping list.")

# Defines function to remove an item from the list if present
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print("Item removed from shopping list.")
        else:
            print("Item not found in shopping list.")

# Defines function to view the list
    def view_list(self):
        if not self.shopping_list:
            print("Shopping list is empty")
        else:
            print("Shopping list: ")
            for item in self.shopping_list:
                print(item)

# Creates pet_store_list object from ShoppingList class
pet_store_list = ShoppingList("Pet Store Shopping List")

# Adds items to shopping_list
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Removes item from shopping_list
pet_store_list.remove_item("flea collars")

# Attempts to add "frisbee" again to shopping_list
pet_store_list.add_item("frisbee")

pet_store_list.view_list()