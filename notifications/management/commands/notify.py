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

class Command(BaseCommand):
    help = 'Sends notifications to phones with saved tokens'

    def handle(self, *args, **options):
        users = Token.objects.all()

        # Get list of daily items 
        daily = scraper.tigerMenusAsDhallList()

        for user in users: 
            matches = matchItems(Token.get_favorites(user), daily)
            if matches:
                send_push_message(user.token, message(matches), extra=None)

        self.stdout.write(self.style.SUCCESS("success"))

def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token, body=message, data=extra)
        )
    except PushServerError as exc: 
        pass
    except (ConnectionError, HTTPError) as exc: 
        pass

    try:
        # We got a response back, but we don't know whether it's an error yet
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        pass

# Creates a message based on the matches in the users' favorite foods and the current items 
def message(matches): 
    message = ""
    for dhall in matches: 
        message += "At " + dhall + ": "
        for item in matches: 
            message += item + ", "
        message = message[:-2]
        message += ". "
    return message


# Determines if there is a match between a list of the users favorites and the daily items
def matchItems(favorites, daily):
    matches = {} 

    for item in daily: 
        if item in favorites: 
            if not dhall in matches: 
                matches[dhall] = []
            matches[dhall].append(item)
    return matches