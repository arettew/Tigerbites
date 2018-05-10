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

def categorize(item, ingredients, allergens):
    category = ""
    if "soup" in item.category.lower():
        category += "Soup"
    elif "salad" in item.category.lower(): 
        category += "Salad"
    elif "entree" in item.category.lower():
        category += "Entree"
    elif "side" in item.category.lower():
        category += "Side"
    
    
    if "vegetarian" in item.category.lower():
        category += "Vegetarian" if category == "" else ", Vegetarian"
    if "vegan" in item.category.lower(): 
        category += "Vegan" if category == "" else ", Vegan"

    if not "Vegetarian" in category and not "Vegan" in category and hasMeat(item.name, ingredients, allergens):
        category += "Meat" if category == "" else ", Meat"
    elif hasDairy(allergens) and not "Meat" in category:
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ", Vegetarian"
    elif not "Meat" in category:
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ", Vegetarian"
        if not "Vegan" in category:
            category += ", Vegan"

    return category

def hasMeat(name, ingredients, allergens):
    if "chicken" in ingredients.lower() or "chicken" in name.lower():
        return True
    if "beef" in ingredients.lower() or "beef" in name.lower():
        return True 
    if "veal" in ingredients.lower() or "veal" in name.lower():
        return True
    if "duck" in ingredients.lower() or "duck" in name.lower():
        return True
    if "ham" in ingredients.lower() or "ham" in name.lower():
        return True
    if "meat" in ingredients.lower():
        return True
    if "fish" in allergens.lower() or "fish" in name.lower():
        return True
    if "shellfish" in allergens.lower(): 
        return True
    if "bacon" in ingredients.lower():
        return True
    if "pork" in ingredients.lower() or "pork" in name.lower():
        return True
    if "turkey" in ingredients.lower() or "turkey" in name.lower(): 
        return True
    if "prosciutto" in ingredients.lower() or "prosciutto" in name.lower():
        return True
    if "hot dog" in ingredients.lower() or "hot dog" in name.lower(): 
        return True
    if "kielbasa" in ingredients.lower() or "kielbasa" in name.lower(): 
        return True
    return False

def hasDairy(allergens):
    if "milk" in allergens.lower():
        return True
    if "egg" in allergens.lower():
        return True