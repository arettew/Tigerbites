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
                f = FoodItem(item.name, item.category, item.meal, item.calories, item.fat, item.protein, item.carbs)
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
    