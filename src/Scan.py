import asyncio
import requests
# from src.Cache import Handler
from src.SQL import Sql

sql = Sql()

class Scan:
    def __init__(self):
        self.panels = sql.Get()

    async def Fetch(self,panel=None):
        if panel == None:
            for p in self.panels:
                result = await self.Check(p)
                sql.Set(p[0],
                        result['online'],
                        str(result['cpu']),
                        str(result['memory']),
                        str(result['disk']))
    
    async def Check(self, panel):
        id = panel[0]

        try:
            request = requests.get("http://" + panel[2] + "/platy/", timeout=2)

            print(panel[0], "online")
            if request.status_code == 404:
                return {"name": panel[1],
                        "online": True,
                        "cpu": 0,
                        "memory": 0,
                        "disk": 0}
            else:
                data = request.json()
                return {"name": panel[1],
                        "online": True,
                        "cpu": data["cpu"],
                        "memory": data["memory"],
                        "disk": data["disk"]}

        except Exception as e:
            print(panel[0], "offline")
            print(e)
            return {"name": panel[1],
                        "online": False,
                        "cpu": 0,
                        "memory": 0,
                        "disk": 0}

s = Scan()
loop = asyncio.get_event_loop()
loop.create_task(s.Fetch())
loop.run_forever()