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
    print(panel)
    id = panel[0]
    res = {}
    offline = ""
    # Iterate through the list of servers
    try:
        # Attempts to fetch platy stats from panel.
        request = requests.get("http://" + panel[2] + config.Get("stats_path"),
                               timeout=config.Get("scan_timeout"))
        print(panel[0], "online")
        offline = "online"
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
        status = "offline"
    
    handler.SetStatus(id,offline,str(cpu),str(memory),str(disk))

    res[panel[0]] = {"name": panel[1],
                 "online": panel[4],
                 "location": panel[3],
                 "cpu": panel[6],
                 "memory":panel[7],
                 "disk":panel[8]}

    return res

  def Loop(self):
    self.Fetch()
    threading.Timer(config.Get("scan_interval"), self.Loop).start()