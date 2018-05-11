from django.core.management.base import BaseCommand, CommandError
from notifications.models import Token

from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

import scraper
import datetime

class Command(BaseCommand):
    help = 'Sends notifications to phones with saved tokens'

    def handle(self, *args, **options):
        users = Token.objects.all()

        # Get list of daily items 
        daily = scraper.tigerMenusAsDhallList()

        for user in users: 
            matches = matchItems(Token.get_favorites(user), daily)
            if matches:
                print(message(matches))
                send_push_message(user.token, message(matches))

        self.stdout.write(self.style.SUCCESS("success"))

def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token, body=message, data=extra)
        )
    except PushServerError as exc: 
        print("invalid")
    except (ConnectionError, HTTPError) as exc: 
        print("Connection or HTTPError")

    try:
        # We got a response back, but we don't know whether it's an error yet
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
        print("Device not registered error")
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        print ("PushResponseError")

# Creates a message based on the matches in the users' favorite foods and the current items 
def message(matches): 
    message = ""
    for dhall in matches: 
        message += "At " + dhall + ": "
        for item in matches[dhall]: 
            message += item + ", "
        message = message[:-2]
        message += ". "
    return message


# Determines if there is a match between a list of the users favorites and the daily items
def matchItems(favorites, daily):
    matches = {} 

    for dhall in daily:
        for item in daily[dhall]: 
            if item in favorites: 
                if not dhall in matches: 
                    matches[dhall] = []
                matches[dhall].append(item)
    return matches