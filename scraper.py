import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
from fooditem import FoodItem
import fooditem
from datetime import datetime, timezone

# Helper method to throw out result if it a meal header 
def isMeal(item):
    if item == "Lunch" or item == "Breakfast" or item == "Dinner":
        return True
    return False

# Scrapes Tiger Menus. The results are returned as a dict of dhalls which contains dict of categories 
# which contain lists of food items 
def scrapeTigerMenus():
    page_url = "https://tigermenus.herokuapp.com/"

    cur_hour = datetime.now(timezone.utc).hour
    cur_day = datetime.now(timezone.utc).weekday()

    # Hours are in UTC 
    BREAKFAST_START = 2
    BREAKFAST_END = 14
    SATURDAY = 5

    if cur_hour >= BREAKFAST_START and cur_hour <= BREAKFAST_END and cur_day < SATURDAY:
        # Tigermenus automatically skips breakfast on weekdays 
        page_url += "breakfast/" + str(cur_day)

    DHALL_DIV_CLASS = "col-sm-2"

    page = urllib.request.urlopen(page_url)
    soup = BeautifulSoup(page, "html.parser")
    menu = soup.find_all("div", class_= DHALL_DIV_CLASS)

    items = {}
    for element in menu:
        food_categories = {}
        current_category = "-- Other --"
        # TigerMenus uses <p></p> tags for menu items and categories 
        for item in element("p"):
            if "--" in item.text:
                # Categories have form "-- Category --"
                food_list = []
                food_categories[item.text] = food_list
                current_category = item.text
            # Discards meal name 
            elif not isMeal(item.text):
                food_categories[current_category].append(item.text)
        # adds all items in dhall to dict 
        dhall = element("h3")[0].text
        items[dhall] = food_categories

    return items

# Takes results from scraping TigerMenus and discards categories. The result is a dictionary 
# of dhalls which each contains a list of items 
def tigerMenusAsDhallList(): 
    scraping_results = scrapeTigerMenus()

    # Convert scraping results to a dict of dhalls with a list of items
    results_list = {}
    for dhall in scraping_results: 
            results_list[dhall] = []
            for category in scraping_results[dhall]:
                for item in scraping_results[dhall][category]:
                    results_list[dhall].append(item)
    
    return results_list

# Scrapes dining services. Begins at the main page and progresses to every viewable meal 
# every time this method is called
def scrapeDiningServices():
    menus_url = "https://campusdining.princeton.edu/dining/_Foodpro/online-menu/"

    menus_page = urllib.request.urlopen(menus_url)
    soup = BeautifulSoup(menus_page, "html.parser")
    
    RES_COLLEGE_ID = "resLocations"
    locations = soup.find_all(id=RES_COLLEGE_ID)

    items = []
    for location in locations: 
        for link in location("a"):
            # Links to each individual dhall page
            scrapeDhallPage(menus_url + link["href"], menus_url, items, link.text.lstrip())
    return items

# Scrapes a res college page. Progresses to each date 
def scrapeDhallPage(page_url, root, items, dhall):
    page = urllib.request.urlopen(page_url)
    soup = BeautifulSoup(page, "html.parser")

    DATE_CLASS = "menuDates"
    days = soup.find_all(class_=DATE_CLASS)

    for day in days:
        # Links to each date on the menu page
        link = re.sub(" ", "%20", day["href"])
        scrapeDay(root + link, root, items, dhall)

# Scrapes a res college page for a specific day. Progresses to a specific meal 
def scrapeDay(day_url, root, items, dhall):
    page = urllib.request.urlopen(day_url)
    soup = BeautifulSoup(page, "html.parser")

    MEAL_CLASS = "card-header"
    meals = soup.find_all(class_=MEAL_CLASS)
    for meal in meals:
        meal_name = meal("a")[0]["name"]
        scrapeMeal(root + meal("a")[0]["href"], root, items, dhall, meal_name)

# Scrapes a specific meal (for specific res college on a specific day). Progresses to an 
# individual item's nutrition page. This page is actually reached through a nutrition link
def scrapeMeal(meal_url, root, items, dhall, meal):
    meal_page = urllib.request.urlopen(meal_url)
    soup = BeautifulSoup(meal_page, "html.parser")

    CATEGORY_CLASS = "pickmenucolmenucat"
    FOOD_CLASS = "pickmenucoldispname"

    meal_items = soup.find_all("div")
    category = ""

    for item in meal_items:
        if item.has_attr("class"):
            if item["class"][0] == CATEGORY_CLASS:
                category = item.text
            if item["class"][0] == FOOD_CLASS:
                for key in item:
                    if key.has_attr("href"):
                            scrapeFoodItem(root + key["href"], dhall, items, meal, category)

# Scrapes the item needed for a specific food item from its nutrition page 
def scrapeFoodItem(item_url, dhall, items, meal, category):
    item_page = urllib.request.urlopen(item_url)
    soup = BeautifulSoup(item_page, "html.parser")

    item = FoodItem()

    item.meal = meal
    item.dhall = dhall

    name = soup.find("h2").text
    if (name == ""):
        # Some items don't have any nutritional information. These items are usually boring. 
        # Don't continue with them 
        return
    item.name = name

    facts2 = soup.find_all(id="facts2")
    for fact in facts2: 
        if fact.b:
            try: 
                # Gets numeric value of calories 
                calorie_info = fact.b.text.split()
                calories = calorie_info[len(calorie_info) - 1]
                item.calories = calories
            except: 
                item.calories = 0 
    
    facts4 = soup.find_all(id="facts4")
    for fact in facts4:
        if ("Total Fat" in fact.text):
            try: 
                # Gets numeric value of fat and discards the "g"
                fat_info = fact.text.split()
                fat = fat_info[len(fat_info) - 1][:-1]
                item.fat = fat
            except: 
                item.fat = 0
        elif ("Protein" in fact.text):
            try: 
                # Gets numeric value of fat and discards the "g"
                protein_info = fact.text.split()
                protein = protein_info[len(protein_info) - 1][:-1]
                item.protein = protein
            except: 
                item.protein = 0 
        elif ("Carb" in fact.text):
            try: 
                # Gets numeric value of carbs and discards the "g"
                carb_info = fact.text.split()
                carbs = carb_info[len(carb_info) - 1][:-1]
                item.carbs = carbs
            except: 
                item.carbs = 0 

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

    item.allergens = allergens_text
    item.ingredients = ingredients_text
    # Dining services category is used to categorize with our own categories then is overwritten
    item.category = category
    item.category = fooditem.categorize(item)

    items.append(item)