# Create your tests here.

from django.test import TestCase, RequestFactory
from .views import token
from food.models import FoodItem
 
import json
# Create your tests here.
 
class PostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        request = self.factory.post('/notifications', json.dumps({'to': 'ExponentPushToken[s28t0zDF95W7OMjk6hCiv1]', 'title': 'food', 'data': {'button': False}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 202)