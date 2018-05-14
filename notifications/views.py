from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json 

from notifications.models import Token
from food.models import FoodItem 

@csrf_exempt
def token(request):
    if request.method == 'POST':
        try:
            post_data = json.loads(request.body)

            # Does this request take the form we except from our app? 
            if not "to" in post_data: 
                return HttpResponse(status=400)
            elif not "title" in post_data:
                return HttpResponse(status=400)

            token_val = post_data["to"]
            name = post_data["title"]

            # Validate that the this appears to be the data we expect
            try: 
                # Test if the token_val appears to be a expo push token 
                if not token_val[:18] == "ExponentPushToken[":
                    return HttpResponse(status=400)
                if not token_val[-1:] == "]":
                    return HttpResponse(status=400)

                #Test if we've stored this item as a food item 
                if not FoodItem.objects.filter(item_name = name).exists(): 
                    return HttpResponse(status=400)
            except: 
                return HttpResponse(status=400)

            if Token.objects.filter(token=token_val).exists(): 
                # User already exists
                user = Token.objects.filter(token=token_val).first()
            
                # Adds or removes from favorites
                favorites = Token.get_favorites(user)
                if name in favorites: 
                    favorites.remove(name)
                else: 
                    favorites.append(name)
            
                Token.set_favorites(user, favorites)
                user.save()
                return HttpResponse(status=202)
            else: 
                # User doesn't already exist within system 
                favorites = [name]
                user = Token(token_val, "")
                Token.set_favorites(user, favorites)    
                user.save()
                return HttpResponse(status=202)

        except: 
            return HttpResponse(status=400)

    # Return an empty page in the case of GET request/any other type of request    
    return HttpResponse("")
