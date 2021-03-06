from django.db import models

# Food items that can be served on campus
class FoodItem(models.Model):
   item_name = models.CharField(max_length=200, default="", primary_key=True)
   category = models.CharField(max_length=200, default="")
   meal = models.CharField(max_length=15, default="")
   dhall = models.CharField(max_length = 200, default = "")
   calories = models.IntegerField(default=0)
   fat = models.FloatField(default=0)
   protein = models.FloatField(default=0)
   carbs = models.FloatField(default=0)
   ingredients = models.CharField(max_length = 2000, default = "")
   allergens = models.CharField(max_length = 2000, default = "")
