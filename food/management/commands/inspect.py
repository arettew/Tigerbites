from django.core.management.base import BaseCommand, CommandError
from food.models import FoodItem 

class Command(BaseCommand):
    help = 'Helps to inspect database items'

    def handle(self, *args, **options):
        # Print any item categorized as Vegetarian 
        items = FoodItem.objects.filter(category__contains = 'Vegetarian')

        for item in items: 
            print(item.item_name)
            
        self.stdout.write(self.style.SUCCESS("Success"))