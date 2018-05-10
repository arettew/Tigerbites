from django.test import TestCase, RequestFactory
from .views import token

import json
# Create your tests here.

class PostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_details(self):
        request = self.factory.post('/notifications', json.dumps({'token': {'value': 'token'}, 'user': {'userData': {'button': False, "name": 'food'}}}), content_type='application/json')
        response = token(request)
        self.assertEqual(response.status_code, 200)

