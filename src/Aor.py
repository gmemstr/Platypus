import tornado.ioloop
import tornado.websocket
import json
import ServerHandler
import Slackbot

sql = ServerHandler.Sql()
AliveSockets = set()


class Aor(tornado.websocket.WebsocketHandler):

    def open(self):
        print(self.request.remote_ip, "connected to AOR, awaiting authentication")
        try:
            self.server = sql.Ip(self.request.remote_ip)
        except:
            print(self.request.remote_ip,
                  "socket closed, unable to find ip in database")
            self.close()

    def on_message(self, message):
        try:
            message = json.loads(message)
        except:
            self.write_message('{"success":false,"message":"invalid_message"}')

        if self.server["verified"]:
            j = json.dumps({
                "id": self.server["id"],
                "online": True,
                "cpu": message["cpu"],
                "disk": message["disk"],
                "memory": message["memory"]
            })
            SendFetchMessage(j)
            self.write_message('{"success":true,"message":"recieved_stats"}')

        else:
            if message["masterkey"] == config.Get["masterkey"]:
                print(self.server["name"], "registered uuid", message["uuid"])
                sql.Register(self.server, message["uuid"])
                self.write_message(
                    '{"success":true,"message":"registered_uuid"}')

    def on_close(self):
        print(self.server["name"], "disconnected, assuming offline!")
        j = json.dumps({
            "id": self.server["id"],
            "online": False,
            "cpu": 0,
            "disk": 0,
            "memory": 0
        })
        SendFetchMessage(j)


class FetchWebsocket(tornado.websocket.WebSocketHandler):

    def open(self):
        AliveSockets.add(self)
        print("Fetch websocket opened - client " + self.request.remote_ip)

    def on_message(self, message):
        print(self.request.remote_ip + " requested panel " + message)
        # res = scan.Fetch(message)
        res = "placeholder"
        self.write_message(res)
        print(self.request.remote_ip + " was sent " + message)

    def on_close(self):
        AliveSockets.remove(self)
        print("Fetch websocket closed - client " + self.request.remote_ip)


def SendFetchMessage(message):
    for ws in AliveSockets:
        ws.write_message(message)
