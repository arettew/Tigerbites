from django.db import models

# Create your models here.

class FoodItem(models.Model):
   item_name = models.CharField(max_length=150, default="", primary_key=True)
   category = models.CharField(max_length=200, default="")
   meal = models.CharField(max_length=15, default="")
   dhall = models.CharField(max_length = 100, default = "")
   calories = models.IntegerField(default=0)
   fat = models.FloatField(default=0)
   protein = models.FloatField(default=0)
   carbs = models.FloatField(default=0)

   def __str__(self):
       return self.item_name
