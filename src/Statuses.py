import requests
import threading
import json
from Cache import Stash
import re


def Scan():
    # New scan method incorporates server stats
    # from new custom script located on each panel
    # hopefully
    file = open("json/servers.json", "r").read()
    s_list = json.loads(file)

    s_stats = {}  # Collection of all panels and their status

    for s in s_list:
        # Iterate through the list of servers
        try:
            # @TODO write custom script for servers
            request = requests.get("http://" + s["hostname"] + "/platy/",
                                   timeout=1)  # Timeout of 1 second
            print(s["name"] + " - online")

            # Strip out int from name of panel
            s_num = int(re.search(r'\d+', s["name"]).group())

            s_stats[s_num] = {"location": s["location"],
                              "online": True,
                              "cpu": 34,  # CPU
                              "mem": 42,  # RAM
                              "disk": 42}  # Disk
            # Outputted JSON:
            # [ "3": {"cpu":34,"mem":42,"disk":42} ]
            # Filters out just the int from the name
            # for easier sorting later

        except:
            # If panel is down, the request will throw an
            # exception. We handle that exception by marking
            # the panel as "down" in cache and setting values
            # to zero.
            print(s["name"] + " - too long to respond (1s)")
            s_num = int(re.search(r'\d+', s["name"]).group())
            s_stats[s_num] = {"location": s["location"],
                              "online": False,
                              "cpu": 0,  # CPU
                              "mem": 0,  # RAM
                              "disk": 0}  # Disk

    # Stash results
    Stash(s_stats, "json/stats.json", False)

    return "Done"  # Don't really need to return anything
    # But... well... I don't know why I do


# Look function for scanning every 300 seconds
# or 5 minutes
def Loop():
    Scan()
    threading.Timer(300, Loop).start()

# Finally call loop function
Loop()
