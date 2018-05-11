class FoodItem: 
    name = ""
    category = ""
    meal = ""
    calories = ""
    protein = ""
    carbs = ""
    fat = ""
    dhall = ""
    ingredients = ""
    allergens = "" 

# Assigns categories to the FoodItem passed as an argument 
def categorize(item):
    category = ""
    if "soup" in item.category.lower() or "soup" in item.name.lower():
        category += "Soup"
    elif "salad" in item.category.lower() or "salad" in item.name.lower(): 
        category += "Salad"
    elif "entree" in item.category.lower():
        category += "Entree"
    elif "side" in item.category.lower():
        category += "Side"
    
    
    if "vegetarian" in item.category.lower():
        category += "Vegetarian" if category == "" else ", Vegetarian"
    if "vegan" in item.category.lower(): 
        category += "Vegan" if category == "" else ", Vegan"

    if not "Vegetarian" in category and not "Vegan" in category and hasMeat(item):
        # Item has meat 
        category += "Meat" if category == "" else ", Meat"
    elif hasDairy(item) and not "Meat" in category:
        # Item is vegetarian but not vegan 
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ", Vegetarian"
    elif not "Meat" in category:
        # Item is vegan and vegetarian 
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ", Vegetarian"
        if not "Vegan" in category:
            category += ", Vegan"

    return category

# Attempts to determine whether this item contains meat 
def hasMeat(item):
    if "meatless" in item.name.lower(): 
        return False
    if "chicken" in item.ingredients.lower() or "chicken" in item.name.lower():
        return True
    if "beef" in item.ingredients.lower() or "beef" in item.name.lower():
        return True 
    if "veal" in item.ingredients.lower() or "veal" in item.name.lower():
        return True
    if "duck" in item.ingredients.lower() or "duck" in item.name.lower():
        return True
    if "ham" in item.ingredients.lower() or "ham" in item.name.lower():
        return True
    if "meat" in item.ingredients.lower():
        return True
    if "fish" in item.allergens.lower() or "fish" in item.name.lower():
        return True
    if "shellfish" in item.allergens.lower(): 
        return True
    if "bacon" in item.ingredients.lower():
        return True
    if "pork" in item.ingredients.lower() or "pork" in item.name.lower():
        return True
    if "turkey" in item.ingredients.lower() or "turkey" in item.name.lower(): 
        return True
    if "prosciutto" in item.ingredients.lower() or "prosciutto" in item.name.lower():
        return True
    if "hot dog" in item.ingredients.lower() or "hot dog" in item.name.lower(): 
        return True
    if "kielbasa" in item.ingredients.lower() or "kielbasa" in item.name.lower(): 
        return True
        
    return False

# Determines whether this item has milk or eggs 
def hasDairy(item):
    # Dhalls uniformly list these items in allergens 
    if "milk" in item.allergens.lower():
        return True
    if "egg" in item.allergens.lower():
        return True