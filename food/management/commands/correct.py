from django.core.management.base import BaseCommand, CommandError
from food.models import FoodItem 

class Command(BaseCommand):
    help = 'Correct any mistakes that may have occurred within saving items'

    def handle(self, *args, **options):
        self.stdout.write("Removing excess commas...")
        all_items = FoodItem.objects.all()
        for item in all_items: 
            if item.dhall != "" and item.dhall[0] == ",":
                item.dhall = item.dhall[1:]
                item.save()
        self.stdout.write("Finished")
