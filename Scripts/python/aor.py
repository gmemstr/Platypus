import json
from websocket import create_connection

ws = create_connection("ws://localhost:8888/aor")
ws.send("{}")
result = ws.recv()
