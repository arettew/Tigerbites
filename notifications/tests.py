from django.test import TestCase, RequestFactory
from .views import token
from food.models import FoodItem
from unittest.mock import MagicMock

import json
# Create your tests here.
