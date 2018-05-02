from django.shortcuts import render
from django.http import HttpResponse
from scraper import scrapeTigerMenus
from food.models import FoodItem
import json 
import datetime

# Create your views here.
def today(request):
    food = scrapeTigerMenus()
    return HttpResponse(json.dumps(food))

def all(request):
    results = FoodItem.objects.values()
    list_results = list(results)
    return HttpResponse(json.dumps(sorted(list_results, key = lambda i: i['item_name'])))