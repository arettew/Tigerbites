from django.shortcuts import render
from django.http import HttpResponse
import json 

from notifications.models import Token

# Create your views here.

def token(request):
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)
            # Does this have all the information we expect? 
            if not "to" in post_data: 
                return HttpResponse(status=400)
            elif not "title" in post_data:
                return HttpResponse(status=400)
            elif not "data" in post_data:
                return HttpResponse(status=400)

            token_val = post_data["to"]
            name = post_data["title"]
            button = post_data["data"]["button"]

            if Token.objects.filter(token=token_val).exists(): 
                # User exists
                user = Token.objects.filter(token=token_val).first()
            
                # Adds or removes from favorites
                favorites = user.favorites
                if not button:
                    favorites.append(name)
                else:
                    favorites.remove(name)
                user.favorites = favorites

                user.save()
                return HttpResponse(status=202)
            else: 
                # User doesn't already exist within system 
                favorites = [name]
                user = Token(token_val, favorites)    
                user.save()
                return HttpResponse(status=202)

        except: 
            return HttpResponse(status=400)
        
    return HttpResponse("")
