import tornado.ioloop
import tornado.websocket
import json
import ServerHandler
import Config

config = Config.Config()
sql = ServerHandler.Sql()
AliveSockets = set()


class Aor(tornado.websocket.WebSocketHandler):

    def open(self):
        print(self.request.remote_ip,
              "connected to AOR, awaiting authentication")

        try:
            self.server = sql.Ip(self.request.remote_ip)
            self.write_message('{"success":true,"require_auth":"true"}')
        except:
            print(self.request.remote_ip,
                  "socket closed, unable to find IP in database")
            self.close()

    def on_message(self, message):
        try:
            message = json.loads(message)
        except:
            self.write_message('{"success":false,"message":"invalid_message"}')

        if self.server[3] != "":
            j = json.dumps({
                "id": self.server[0],
                "online": True,
                "cpu": message["stats"]["cpu"],
                "disk": message["stats"]["disk"],
                "memory": message["stats"]["memory"]
            })
            SendFetchMessage(j)
            self.write_message('{"success":true,"message":"recieved_stats"}')

        else:
            if message["masterkey"] == config.Get("master_key"):
                print(self.server[1], "registered uuid", message["uuid"])
                sql.Register(self.server, message["uuid"])
                self.write_message(
                    '{"success":true,"message":"registered_uuid"}')
                self.server[3] = message["uuid"]

    def on_close(self):
        if self.server is not None:
            print(self.server[1], "disconnected, assuming offline!")
            j = json.dumps({
                "id": self.server[0],
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
