# Create your tests here.

from django.test import TestCase, RequestFactory
from .views import token
from food.models import FoodItem
from notifications.models import Token
 
import json
# Create your tests here.
 
class PostTestAdd(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        FoodItem.objects.create(item_name='food')
        request = self.factory.post('/notifications', json.dumps({'to': 'ExponentPushToken[token]', 'title': 'food', 'data': {'button': False}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 202)

 
class PostTestRemove(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        FoodItem.objects.create(item_name='food')
        Token.objects.create(token='ExponentPushToken[token]', favorites='["food"]')
        request = self.factory.post('/notifications', json.dumps({'to': 'ExponentPushToken[token]', 'title': 'food', 'data': {'button': True}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 202)

class PostTestNotAToken(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        FoodItem.objects.create(item_name='food')
        request = self.factory.post('/notifications', json.dumps({'to': 'ExponentPushToken[---', 'title': 'food', 'data': {'button': False}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 400)

class PostTestNotAnItem(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        request = self.factory.post('/notifications', json.dumps({'to': 'ExponentPushToken[token]', 'title': 'not_in_database', 'data': {'button': False}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 400)
