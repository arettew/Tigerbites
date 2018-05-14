from django.core.management.base import BaseCommand, CommandError
from notifications.models import Token

from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError

import scraper
import datetime

class Command(BaseCommand):
    help = 'Sends notifications to phones with saved tokens'

    def handle(self, *args, **options):
        users = Token.objects.all()

        # Get list of items for the next meal 
        next_meal = scraper.tigerMenusAsDhallList()

        for user in users: 
            # Find matches to use to send notification
            matches = matchItems(Token.get_favorites(user), next_meal)
            if matches:
                send_push_message(user.token, message(matches))

        self.stdout.write(self.style.SUCCESS("success"))

# Sends push message
def send_push_message(token, message):
    # Send the message 
    try:
        response = PushClient().publish(PushMessage(to=token, body=message, data=None))
    except:
        print("An error occurred when trying the send the message")

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        # Remove push token from database 
        Token.objects.filter(token=token).delete()
        print("Device not registered error")
    except PushResponseError:
        print("There was a response error")

# Creates a message based on the matches in the users' favorite foods and the current items 
def message(matches): 
    message = ""

    for dhall in matches: 
        message += "At " + dhall + ": "
        foods = "" 
        if len(matches[dhall]) < 3:
            for item in matches[dhall]: 
                foods += item + ", "
                # Removes last comma and space
            foods = foods[:-2] + ". "
        else: 
            foods = str(len(matches[dhall])) + " items. "
        message += foods
    return message


# Determines if there is a match between a list of the user's favorites and the daily items
def matchItems(favorites, next_meal):
    matches = {} 

    for dhall in next_meal:
        for item in next_meal[dhall]: 
            if item in favorites: 
                if not dhall in matches: 
                    matches[dhall] = []
                matches[dhall].append(item)
    return matches