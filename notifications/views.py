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
            if not "token" in post_data: 
                return HttpResponse(status=400)
            elif not "value" in post_data["token"]:
                return HttpResponse(status=400)
            elif not "user" in post_data:
                return HttpResponse(status=400)
            elif not "userData" in post_data["user"]:
                return HttpResponse(status=400)

            token_val = post_data["token"]["value"]
            data = post_data["user"]["userData"]

            if Token.objects.filter(token=token_val).exists(): 
                # User exists
                user = Token.objects.filter(token=token_val).first()
            
                # Adds or removes from favorites
                favorites = user.favorites
                if not data["button"]:
                    favorites.append(data["name"])
                else:
                    favorites.remove(data["name"])
                user.favorites = favorites
                
                user.save()
            else: 
                # User doesn't already exist within system 
                favorites = [data["name"]]
                user = Token(token_val, favorites)    
                user.save()

        except: 
            return HttpResponse(status=400)
        
    return HttpResponse("")
