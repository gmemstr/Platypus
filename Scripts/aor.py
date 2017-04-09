import websocket
import time
import json
import psutil
from time import sleep

glblws = None


def GetStats():
    s = {}
    s["cpu"] = round(psutil.cpu_percent())  # Used CPU
    s["memory"] = round(psutil.virtual_memory().percent)  # Used memory
    s["disk"] = round(psutil.disk_usage('C:\\').percent)  # Used disk
    return s


def on_message(ws, message):
    raw = json.loads(message)
    if raw["success"] is True and raw["require_auth"] is True:
        print("DEBUG", "SENDING DATA")
        stats = GetStats()
        data = {
            "uuid": "5c4e9e72-d3ad-4242-af13-64c4446de457",
            "stats": {
                "cpu": stats["cpu"],
                "disk": stats["disk"],
                "memory": stats["memory"]
            }
        }
        j = json.dumps(data)
        ws.send(j)
        sleep(5)


def on_error(ws, error):
    # print(error)
    pass


def on_close(ws):
    print("Master has gone away")


def on_open(ws):
    glblws = ws
    print("Connected to master")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/aor",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()
