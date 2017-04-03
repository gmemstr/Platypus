import websocket
import time
import json


def on_message(ws, message):
    raw = json.loads(message)
    if raw["success"] is True and raw["require_auth"] is True:
        data = {
            "uuid": "5c4e9e72-d3ad-4242-af13-64c4446de457",
            "stats": {
                "online": True,
                "cpu": 0,
                "disk": 0,
                "memory": 0
            }
        }
        j = json.dumps(data)
        ws.send(j)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("opened connection")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/aor",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()
