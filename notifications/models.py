from django.db import models
import json

# Users and their favorite foods
class Token(models.Model):
    token = models.CharField(max_length=100, default="", primary_key=True)
    favorites = models.TextField(default = "")

    # Sets favorites, passed in as a list, as json
    def set_favorites(self, favorites):
        self.favorites = json.dumps(favorites)

    # Returns favorites, saved as json, as a list 
    def get_favorites(self):
        return json.loads(self.favorites)

