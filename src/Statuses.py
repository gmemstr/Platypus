import requests
import json
from src.Cache import Stash, Fetch
import threading
from src.Config import Config

config = Config()

class Scanning:

  def Scan(self):
    # New scan method incorporates server stats
    # from new custom script located on each panel
    s_list = Fetch("servers", False)
    s_stats = {}

    for s in s_list:
      id = s["id"]
      # Iterate through the list of servers
      try:
          # Attempts to fetch platy stats from panel.
          request = requests.get("http://" + s["hostname"] + config.Get("stats_path"),
                                 timeout=config.Get("scan_timeout"))
          print(s["name"] + " - online")

          # If panel responds with 404, we assume platypus
          # status script was not deployed (properly?)
          if request.status_code == 404:
            s_stats[id] = {"name": s["name"],
                            "location": s["location"],
                            "online": True,
                            "cpu": "n/a",  # CPU
                            "mem": "n/a",  # RAM
                            "disk": "n/a"}  # Disk  
          else:
            data = request.json()
            s_stats[id] = {"name": s["name"],
                              "location": s["location"],
                              "online": True,
                              "cpu": data["cpu"],  # CPU
                              "mem": data["memory"],  # RAM
                              "disk": data["disk"]}  # Disk
          # Outputted JSON:
          # [ "3": {"name": "Panel 3", cpu":34,"mem":42,"disk":42} ]
      except:
          print(s["name"] + " - offline")
          s_stats[id] = {"name": s["name"],
                            "location": s["location"],
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