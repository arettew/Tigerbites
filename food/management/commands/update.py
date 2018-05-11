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

                    if saved_item.dhall == "":
                        saved_item.dhall = item.dhall
                    elif not item.dhall in saved_item.dhall:
                        # Item is served in multiple dhalls
                        if "Graduate" in item.dhall: 
                            # Grad college has space after "Grad College"
                            item.dhall = re.sub("College ", "College", item.dhall)
                        saved_item.dhall += ", " + item.dhall

                    saved_item.category = item.category
                    saved_item.calories = item.calories
                    saved_item.fat = item.fat
                    saved_item.protein = item.protein 
                    saved_item.carbs = item.carbs
                    saved_item.ingredients = item.ingredients
                    saved_item.allergens = item.allergens
                    saved_item.save()
                else:
                    f = FoodItem(item.name, item.category, item.meal, item.dhall, item.calories, item.fat, item.protein, item.carbs, item.ingredients, item.allergens)
                    f.save()

        self.stdout.write(self.style.SUCCESS("Success"))

# Make sure that this item has all the necessary fields 
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

# Make sure these are proper numbers   
def validateNum(possibleNum):
    try:
        float(possibleNum)
        return True
    except ValueError:
        return False