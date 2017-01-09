from slackclient import SlackClient
from Cache import Fetch
import threading

token = "YOUR_SLACK_TOKEN_HERE"
sc = SlackClient(token)


def Post(message, channel, username, icon):
    return sc.api_call(
        "chat.postMessage", channel=channel, text=message,
        username=username, icon_emoji=icon)


def BuildMessage(data):
    channel = "#dept-development"
    username = "Platypus"
    icon = ":desktop_computer:"
    message = "Some panels are offline! "
    for s in data:
        if data[s]['online'] is False:
            message = message + " Panel " + str(s)
    Post(message, channel, username, icon)


def Data():
    data = Fetch("stats", False)
    BuildMessage(data)


def Loop():
    Data()
    threading.Timer(3600, Loop).start()

Loop()
