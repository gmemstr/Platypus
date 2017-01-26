import requests
import json
from src.Cache import Stash
import re
import threading
from src.Config import Config

config = Config()

class Scanning:

  def Scan(self):
    # New scan method incorporates server stats
    # from new custom script located on each panel
    # hopefully
    file = open("src/cache/servers.json", "r").read()
    s_list = json.loads(file)

    s_stats = {}  # Collection of all panels and their status

    for s in s_list:
      # Iterate through the list of servers
      try:
          # Attempts to fetch platy stats from panel.
          # If it results in a 404 we'll handle that with
          # blank statistics, but mark the panel as "online"
          request = requests.get("http://" + s["hostname"] + config.Get("stats_path"),
                                 timeout=config.Get("scan_timeout"))
          print(s["name"] + " - online")

          # Strip out int from name of panel
          s_num = int(re.search(r'\d+', s["name"]).group())
          if request.status_code == 404:
            s_stats[s_num] = {"location": s["location"],
                            "online": True,
                            "cpu": 0,  # CPU
                            "mem": 0,  # RAM
                            "disk": 0}  # Disk  
          else:
            data = request.json()
            s_stats[s_num] = {"location": s["location"],
                              "online": True,
                              "cpu": data["cpu"],  # CPU
                              "mem": data["memory"],  # RAM
                              "disk": data["disk"]}  # Disk
          # Outputted JSON:
          # [ "3": {"cpu":34,"mem":42,"disk":42} ]
          # Filters out just the int from the name
          # for easier sorting later
          # @TODO Write if clause regarding 404
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
    Stash(s_stats, "stats", False)

    return "Done"      

  def Loop(self):
    self.Scan()
    threading.Timer(config.Get("scan_interval"), self.Loop).start()