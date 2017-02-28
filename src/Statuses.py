import requests
import json
from src.Cache import Handler
import threading
from src.Config import Config

config = Config()
handler = Handler()

class Scanning:

  def Fetch(self,panel="all"):
    if panel == "all":
      s_list = handler.Get()
      for s in s_list:
        self.Scan(s)
      return "fs"
    else:
      s = handler.Get(panel)
      return self.Scan(s[0])

  def Scan(self, panel):
    # print(panel)
    id = panel[0]
    res = {}
    online = False
    # Iterate through the list of servers
    try:
      # TODO: Except if stats are not found but page loads (non-404)
        # Attempts to fetch platy stats from panel.
        request = requests.get("http://" + panel[2] + config.Get("stats_path"),
                               timeout=config.Get("scan_timeout"))
        print(panel[0], "online")
        online = True
        if request.status_code == 404:
          cpu = 0  # CPU
          memory = 0  # RAM
          disk = 0  # Disk
        else:
          data = request.json()
          cpu = data["cpu"]  # CPU
          memory = data["memory"]  # RAM
          disk = data["hdd"]  # Disk
    except Exception as e: 
        print(panel[1] + " - offline")
        cpu=0
        disk=0
        memory=0
        online = False
    
    handler.SetStatus(id,online,str(cpu),str(memory),str(disk))

    res[panel[0]] = {"name": panel[1],
                 "online": online,
                 "location": panel[3],
                 "cpu": cpu,
                 "memory":memory,
                 "disk":disk}

    return res

  def Loop(self):
    self.Fetch()
    threading.Timer(config.Get("scan_interval"), self.Loop).start()