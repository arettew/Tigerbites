class FoodItem: 
    name = ""
    category = ""
    meal = ""
    calories = ""
    protein = ""
    carbs = ""
    fat = ""
    dhall = ""

def categorize(item, ingredients, allergens):
    category = ""
    if "soup" in item.category.lower():
        category += "Soup"
    elif "salad" in item.category.lower(): 
        category += "Salad"
    elif "side" in item.category.lower():
        category += "Side"
    elif "entree" in item.category.lower():
        category += "Entree"
    
    if "vegetarian" in item.category.lower():
        category += "Vegetarian" if category == "" else ",Vegetarian"
    if "vegan" in item.category.lower(): 
        category += "Vegan" if category == "" else ",Vegan"

    if not "Vegetarian" in category and not "Vegan" in category and hasMeat(ingredients, allergens):
        category += "Meat" if category == "" else ",Meat"
    elif hasDairy(allergens):
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ",Vegetarian"
    else:
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ",Vegetarian"
        if not "Vegan" in category:
            category += ",Vegan"

    return category

def hasMeat(ingredients, allergens):
    if "chicken" in ingredients.lower():
        return True
    if "beef" in ingredients.lower():
        return True 
    if "veal" in ingredients.lower():
        return True
    if "duck" in ingredients.lower():
        return True
    if "ham" in ingredients.lower():
        return True
    if "meat" in ingredients.lower():
        return True
    if "fish" in allergens.lower():
        return True
    if "shellfish" in allergens.lower(): 
        return True
    if "bacon" in ingredients.lower(): 
        return True
    if "pork" in ingredients.lower(): 
        return True
    return False

def hasDairy(allergens):
    if "milk" in allergens.lower():
        return True
    if "egg" in allergens.lower():
        return True