from slackclient import SlackClient
from src.Cache import Fetch
from src.Config import Config
import threading

config = Config()
channel = config.Get("slack_channel")
token = config.Get("slack_api_key")
sc = SlackClient(token)

class Bot:

    def Post(self,message, channel, username, icon):
        return sc.api_call(
            "chat.postMessage", channel=channel, text=message,
            username=username, icon_emoji=icon)


    def BuildMessage(self,data):
        post = True
        off = 0
        channel = "@gabes"
        username = "Platypus"
        icon = ":desktop_computer:"
        message = "Some panels may be offline!"
        for s in sorted(data):
            if data[s]['online'] is False:
                message = message + " Panel " + str(s)
                off = off + 1

            if off > 1: post = True
            else: post = False

        if post is True: self.Post(message, channel, username, icon)


    def Data(self):
        data = Fetch("stats", False)
        self.BuildMessage(data)

    def Loop(self):
        self.Data()
        threading.Timer(3600, self.Loop).start()
