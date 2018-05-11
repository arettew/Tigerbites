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

        #  Remove commas at the beginning of fields 
        if arg == 'commas':
            self.stdout.write("Removing excess commas...")
            all_items = FoodItem.objects.all()
            for item in all_items: 
                if item.dhall != "" and item.dhall[0:2] == ", ":
                    item.dhall = item.dhall[2:]
                elif item.dhall != "" and item.dhall[0] == ",":
                    item.dhall = item.dhall[1:]
                item.save()
            self.stdout.write("Finished")

        # One time only -  recategorize the items currently in the database with our own 
        # categories 
        elif arg == "recategorize":
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
                    category += "Vegetarian" if category == "" else ", Vegetarian"
                if "vegan" in item.category.lower(): 
                    category += "Vegan" if category == "" else ", Vegan"

                if not "Vegan" in category and not "Vegetarian" in category:
                    if fooditem.hasMeat(item.item_name, item.item_name):
                        # Don't have access to allergens/ingredients for this set 
                        category += "Meat" if category == "" else ", Meat"
                
                if category == "":
                    category += "Side"
                item.category = category 
                item.save()
            self.stdout.write("Finished")

        # Add space after commas in relevant fields 
        elif arg == "space_after_commas":
            self.stdout.write("Adding spaces after commas...")
            all_items = FoodItem.objects.all()
            for item in all_items: 
                item.category = re.sub(",", ", ", item.category)
                item.dhall = re.sub(",", ", ", item.dhall)
                item.save()
            self.stdout.write("Finished")

        # Remove space if there is more than one space in a row 
        elif arg == "remove_space":
            self.stdout.write("Removing excess space...")
            all_items = FoodItem.objects.all()
            for item in all_items:
                item.category = re.sub(" +", " ", item.category)
                item.dhall = re.sub(" +", " ", item.dhall)
                item.save()
            self.stdout.write("Finished")
        
        # One time - Remove space after "Grade College " in current categories
        elif arg == "grad":
            self.stdout.write("Removing space after \"Grad College")
            all_items = FoodItem.objects.all()
            for item in all_items:
                item.dhall = re.sub("Graduate College ", "Graduate College", item.dhall)
                item.save()
        
        # Any other argument 
        else: 
            self.stdout.write("Not a valid correction")
            return

        self.stdout.write(self.style.SUCCESS("Success"))
