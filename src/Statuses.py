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

    s_stats = {}  # Collection of up panels and their status

    for s in s_list:
        # Iterate through the list of servers
        try:
            # @TODO write custom script for servers
            # and implement path of script here --v
            request = requests.get("http://" + s["hostname"],
                                   timeout=1)  # Timeout of 1 second
            print(s["name"] + " - online")
            # s_stat = request.json()
            s_num = int(re.search(r'\d+', s["name"]).group())
            s_stats[s_num] = {"location": s["location"],
                              "online": True,
                              "cpu": 34,  # CPU
                              "mem": 42,  # RAM
                              "disk": 42}  # Disk
            # Outputted JSON:
            # [ "Panel 3": {"cpu":75,"mem":70,"disk":65} ]
            # Values in percentages used

        except:
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


def Loop():
    Scan()
    # Call loop again in 5 minutes
    threading.Timer(300, Loop).start()

Loop()
