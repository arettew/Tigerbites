from django.shortcuts import render
from django.http import HttpResponse
import json 

from notifications.models import Token

# Create your views here.

def token(request):
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            if not "token" in post_data: 
                return HttpResponse(status=400)
            elif not "value" in post_data["token"]:
                return HttpResponse(status=400)
            token = Token(post_data["token"]["value"])
            token.save()
        except: 
            return HttpResponse(status=400)
        
    return HttpResponse("")
