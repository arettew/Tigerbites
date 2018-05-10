from django.shortcuts import render
from django.http import HttpResponse
from scraper import scrapeTigerMenus
from food.models import FoodItem
import json 
import datetime

# Create your views here.
def today(request):
    scraping_results = scrapeTigerMenus()
    all_items = list(FoodItem.objects.all().values_list('item_name', flat=True))
    
    food = {}

    # Get the index number of the item in the database 
    for dhall in scraping_results: 
        if not dhall in food: 
            food[dhall] = {}
        for category in scraping_results[dhall]:
            if not category in food[dhall]:
                food[dhall][category] = {}
            for item in scraping_results[dhall][category]:
                # Check if we've stored this item 
                try:
                    index = all_items.index(item)
                    food[dhall][category][item] = index
                except: 
                    scraping_results[dhall][category].remove(item)
    return HttpResponse(json.dumps(food))

def all(request):
    results = FoodItem.objects.values()
    list_results = list(results)
    return HttpResponse(json.dumps(sorted(list_results, key = lambda i: i['item_name'])))