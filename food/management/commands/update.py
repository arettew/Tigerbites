from django.core.management.base import BaseCommand, CommandError
from food.models import FoodItem 
import scraper 

class Command(BaseCommand):
    help = 'Updates the database with the current week\'s food items'

    def handle(self, *args, **options):
        self.stdout.write("Scraping started...")
        foodItems = scraper.scrapeDiningServices()
        self.stdout.write("Scraping finished...")
        for item in foodItems: 
            if (validateItem(item)):
                if FoodItem.objects.filter(item_name = item.name).exists():
                    # if it exists, update the fields
                    saved_item = FoodItem.objects.get(item_name = item.name)
                    if item.dhall == "":
                        saved_item.dhall = item.dhall
                    elif not item.dhall in saved_item.dhall:
                        # item might be served in multiple dhalls 
                        saved_item.dhall += "," + item.dhall
                    saved_item.category = categorize(item)
                    saved_item.calories = item.calories
                    saved_item.fat = item.fat
                    saved_item.protein = item.protein 
                    saved_item.carbs = item.carbs
                    saved_item.save()
                    #self.stdout.write("Updating " + item.name + "...")
                    self.stdout.write(item.name + ": " + saved_item.category)
                else:
                    f = FoodItem(item.name, categorize(item), item.meal, item.dhall, item.calories, item.fat, item.protein, item.carbs)
                    #self.stdout.write("Saving " + item.name + "...")
                    self.stdout.write(item.name + ": " + f.category)
                    f.save()

        self.stdout.write(self.style.SUCCESS("Success"))

def validateItem(item):
    if (item.name == ""):
        return False
    if (item.category == ""):
        return False
    if (item.meal == ""):
        return False
    if not item.calories.isdigit():
        return False
    if not validateNum(item.fat):
        return False
    if not validateNum(item.protein):
        return False
    if not validateNum(item.carbs):
        return False
    return True
    
def validateNum(possibleNum):
    try:
        float(possibleNum)
        return True
    except ValueError:
        return False

def categorize(item):
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

    if not "Vegetarian" in category and not "Vegan" in category and hasMeat(item):
        category += "Meat" if category == "" else ",Meat"
    elif hasDairy(item):
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ",Vegetarian"
    else:
        if not "Vegetarian" in category:
            category += "Vegetarian" if category == "" else ",Vegetarian"
        if not "Vegan" in category:
            category += ",Vegan"

    return category

def hasMeat(item):
    if "chicken" in item.ingredients.lower():
        return True
    if "beef" in item.ingredients.lower():
        return True 
    if "veal" in item.ingredients.lower():
        return True
    if "duck" in item.ingredients.lower():
        return True
    if "ham" in item.ingredients.lower():
        return True
    if "meat" in item.ingredients.lower():
        return True
    if "fish" in item.allergens.lower():
        return True
    if "shellfish" in item.allergens.lower(): 
        return True
    if "bacon" in item.ingredients.lower(): 
        return True
    if "pork" in item.ingredients.lower(): 
        return True
    return False

def hasDairy(item):
    if "milk" in item.allergens.lower():
        return True
    if "egg" in item.allergens.lower():
        return True
    