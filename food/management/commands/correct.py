from django.core.management.base import BaseCommand, CommandError
from food.models import FoodItem 
import fooditem
import re

class Command(BaseCommand):
    help = 'Correct any mistakes that may have occurred within saving items'

    def add_arguments(self, parser):
        parser.add_argument('correction', nargs=1, type=str, help='correct data')

    def handle(self, *args, **options):
        arg = options['correction'][0]
        #  One time correction - remove commas at 
        if arg == 'commas':
            self.stdout.write("Removing excess commas...")
            all_items = FoodItem.objects.all()
            for item in all_items: 
                if item.dhall != "" and item.dhall[0] == ",":
                    item.dhall = item.dhall[1:]
                    item.save()
            self.stdout.write("Finished")
        # One time correction - recategorize the items currently in the database
        elif arg == "categories":
            self.stdout.write("Beginning recategorizations...")
            all_items = FoodItem.objects.all()
            for item in all_items: 
                category = ""
                if "entree" in item.category.lower():
                    category += "Entree"
                elif "salad" in item.category.lower():
                    category += "Salad"
                elif "side" in item.category.lower():
                    category += "Side"
                elif "soup" in item.category.lower(): 
                    category += "Soup"
                
                if "vegetarian" in item.category.lower():
                    category += "Vegetarian" if category == "" else ",Vegetarian"
                if "vegan" in item.category.lower(): 
                    category += "Vegan" if category == "" else ",Vegan"

                if not "Vegan" in category and not "Vegetarian" in category:
                    if fooditem.hasMeat(item.item_name, item.item_name):
                        # Don't have access to allergens/ingredients for this set 
                        category += "Meat" if category == "" else ",Meat"
                
                if category == "":
                    category += "Side"
                item.category = category 
                item.save()
            self.stdout.write("Finished")
        # One time correction. Add space after commas in relevant fields 
        elif arg == "space":
            self.stdout.write("Adding spaces after commas...")
            all_items = FoodItem.objects.all()
            for item in all_items: 
                item.category = re.sub(",", ", ", item.category)
                item.dhall = re.sub(",", ", ", item.dhall)
                self.stdout.write(item.name)
                item.save()
            self.stdout.write("Finished")
        else: 
            self.stdout.write("Not a valid correction")
            return

        self.stdout.write(self.style.SUCCESS("Success"))
