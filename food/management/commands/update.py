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
                    saved_item.category = item.category
                    saved_item.calories = item.calories
                    saved_item.fat = item.fat
                    saved_item.protein = item.protein 
                    saved_item.carbs = item.carbs
                    saved_item.save()
                    self.stdout.write("Updating " + item.name + "...")
                else:
                    f = FoodItem(item.name, item.category, item.meal, item.dhall, item.calories, item.fat, item.protein, item.carbs)
                    self.stdout.write("Saving " + item.name + "...")
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