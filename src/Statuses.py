import requests
import json
from src.Cache import Handler
import threading
from src.Config import Config

config = Config()
handler = Handler()

class Scanning:

  def Scan(self):
    # New scan method incorporates server stats
    # from new custom script located on each panel
    s_list = handler.Get()
    s_stats = ""

    for s in s_list:
      id = s[0]
      offline = ""
      # Iterate through the list of servers
      try:
          # Attempts to fetch platy stats from panel.
          request = requests.get("http://" + s[2] + config.Get("stats_path"),
                                 timeout=config.Get("scan_timeout"))
          print(s[0], s[2])
          offline = "online"
          # If panel responds with 404, we assume platypus
          # status script was not deployed (properly?)
          if request.status_code == 404:
            s_stats = {"cpu": "n/a",  # CPU
                          "mem": "n/a",  # RAM
                          "disk": "n/a"}  # Disk  
          else:
            data = request.json()
            s_stats = {"cpu": data["cpu"],  # CPU
                            "mem": data["memory"],  # RAM
                            "disk": data["hdd"]}  # Disk
      except Exception as e: 
          print(str(e))
          print(s[1] + " - offline")
          s_stats = {"cpu": 0,  # CPU
                         "mem": 0,  # RAM
                         "disk": 0}  # Disk
          status = "offline"
          
      handler.SetStatus(id,offline,s_stats)

    return "Done"      

  def Loop(self):
    self.Scan()
    threading.Timer(config.Get("scan_interval"), self.Loop).start()