import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
from fooditem import FoodItem
import fooditem
from datetime import datetime, timezone

def isMeal(item):
    if item == "Lunch" or item == "Breakfast" or item == "Dinner":
        return True
    return False

def scrapeTigerMenus():
    page_url = "https://tigermenus.herokuapp.com/"

    cur_hour = datetime.now(timezone.utc).hour
    cur_day = datetime.now(timezone.utc).weekday()

    BREAKFAST_START = 9
    BREAKFAST_END = 13
    SATURDAY = 5

    if cur_hour > BREAKFAST_START and cur_hour < BREAKFAST_END and cur_day < SATURDAY:
        # Tigermenus automatically skips breakfast on weekdays 
        page_url += "breakfast/" + str(cur_day)

    page = urllib.request.urlopen(page_url)

    soup = BeautifulSoup(page, "html.parser")
    # dhalls are separated by divds with this class
    menu = soup.find_all("div", class_= "col-sm-2")

    dhalls = {}
    for element in menu:
        food_categories = {}
        current_category = "-- Other --"
        for item in element("p"):
            if "--" in item.text:
                food_list = []
                food_categories[item.text] = food_list
                current_category = item.text
            elif not isMeal(item.text):
                # discard "Lunch/Breakfast/Dinner" text
                food_categories[current_category].append(item.text)
        # adds all items in dhall to dict 
        dhalls[element("h3")[0].text] = food_categories

    return dhalls

def tigerMenusAsDhallList(): 
    scraping_results = scrapeTigerMenus()

    # Convert scraping results to a dict of dhalls with a list of items
    daily = {}
    for dhall in scraping_results: 
            daily[dhall] = []
            for category in scraping_results[dhall]:
                for item in scraping_results[dhall][category]:
                    daily[dhall].append(item)
    
    return daily

#-----------------------------------------------------------------------------------

def scrapeDiningServices():
    menus_url = "https://campusdining.princeton.edu/dining/_Foodpro/online-menu/"

    menus_page = urllib.request.urlopen(menus_url)
    soup = BeautifulSoup(menus_page, "html.parser")
    
    items = []
    locations = soup.find_all(id="resLocations")
    for location in locations: 
        for link in location("a"):
            # Links to each individual dhall page
            scrapeDhallPage(menus_url + link["href"], menus_url, items, link.text.lstrip())
    return items

def scrapeDhallPage(page_url, root, items, dhall):
    page = urllib.request.urlopen(page_url)
    soup = BeautifulSoup(page, "html.parser")

    days = soup.find_all(class_="menuDates")
    for day in days:
        # Links to each date on the menu page
        link = re.sub(" ", "%20", day["href"])
        scrapeDay(root + link, root, items, dhall)

def scrapeDay(day_url, root, items, dhall):
    page = urllib.request.urlopen(day_url)
    soup = BeautifulSoup(page, "html.parser")

    meals = soup.find_all(class_="card-header")
    for meal in meals:
        scrapeMeal(root + meal("a")[0]["href"], root, items, dhall, meal("a")[0]["name"])

def scrapeMeal(meal_url, root, items, dhall, meal):
    meal_page = urllib.request.urlopen(meal_url)
    soup = BeautifulSoup(meal_page, "html.parser")

    CATEGORY_CLASS = "pickmenucolmenucat"
    FOOD_CLASS = "pickmenucoldispname"

    meal_items = soup.find_all("div")
    count = 0
    category = ""
    for item in meal_items:
        if item.has_attr("class"):
            if item["class"][0] == CATEGORY_CLASS:
                category = item.text
            if item["class"][0] == FOOD_CLASS:
                for key in item:
                    if key.has_attr("href"):
                            scrapeFoodItem(root + key["href"], dhall, items, meal, category)


def scrapeFoodItem(item_url, dhall, items, meal, category):
    item_page = urllib.request.urlopen(item_url)
    soup = BeautifulSoup(item_page, "html.parser")

    item = FoodItem()

    item.meal = meal
    item.dhall = dhall

    name = soup.find("h2").text
    if (name == ""):
        return
    item.name = name

    facts2 = soup.find_all(id="facts2")
    for fact in facts2: 
        if fact.b:
            # This is the calorie amount 
            calorie_info = fact.b.text.split()
            calories = calorie_info[len(calorie_info) - 1]
            if (len(calories) == 0):
                calories = 0
            else:
                item.calories = calories
    
    facts4 = soup.find_all(id="facts4")
    for fact in facts4:
        if ("Total Fat" in fact.text):
            fat_info = fact.text.split()
            fat = fat_info[len(fat_info) - 1][:-1]
            if (len(fat) == 0):
                item.fat = 0
            else: 
                item.fat = fat
        elif ("Protein" in fact.text):
            protein_info = fact.text.split()
            protein = protein_info[len(protein_info) - 1][:-1]
            if (len(protein) == 0):
                item.protein = 0
            else:
                item.protein = protein
        elif ("Carb" in fact.text):
            carb_info = fact.text.split()
            carbs = carb_info[len(carb_info) - 1][:-1]
            if (len(carbs) == 0):
                item.carbs = 0
            else:
                item.carbs = carbs

    ALLERGENS_CLASS = "labelallergensvalue"
    INGREDIENTS_CLASS = "labelingredientsvalue"

    allergens = soup.find(class_ = ALLERGENS_CLASS)
    ingredients = soup.find(class_ = INGREDIENTS_CLASS)
    if allergens is None: 
        allergens_text = ""
    else:
        allergens_text = allergens.text
    if ingredients is None: 
        ingredients_text = ""
    else: 
        ingredients_text = ingredients.text

    item.category = category
    item.allergens = allergens_text
    item.ingredients = ingredients_text
    item.category = fooditem.categorize(item, ingredients_text, allergens_text)
    items.append(item)