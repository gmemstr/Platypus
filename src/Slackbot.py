from slackclient import SlackClient
from src.SQL import Sql
from src.Config import Config
import threading

config = Config()
channel = config.Get("slack_channel")
token = config.Get("slack_api_key")
sc = SlackClient(token)
sql = Sql()

class Bot:
    def Post(self,message, channel, username, icon):
        return sc.api_call(
            "chat.postMessage", channel=channel, text=message,
            username=username, icon_emoji=icon)


    def ServerReport(self,data):
        servers = sql.Get()
        post = True
        off = 0
        channel = config.Get("slack_channel")
        icon = ":desktop_computer:"
        message = "Some panels may be offline!"
        
        for s in servers:
            if s[4] == 0:
                message = message + " " + s[1] + " (" + s[2] + ")"
                off = off + 1

            if off > 1: post = True
            else: post = False

            if off >= 2: icon = ":exclamation:"
            if off >= 4: icon = ":fire:"

        username = "Platypus (" + str(off) + ")"
        if post is True: self.Post(message, channel, username, icon)


    def Loop(self):
        self.ServerReport()
        threading.Timer(config.Get("slack_interval"), self.Loop).start()
