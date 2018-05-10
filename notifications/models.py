from django.db import models
import json

# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=100, default="", primary_key=True)
    # This will be a json string
    favorites = models.TextField(default = "")

    def set_favorites(self, x):
        self.favorites = json.dumps(x)

    def get_favorites(self):
        return json.loads(self.favorites)

