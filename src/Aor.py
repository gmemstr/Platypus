import tornado.ioloop
import tornado.websocket
import json
import ServerHandler

sql = ServerHandler.Sql()
cache = ServerHandler.Cache()
AliveSockets = set()


class AorMaster(tornado.websocket.WebSocketHandler):

    def open(self):
        print(self.request.remote_ip + " connected, asking for authentication...")
        self.write_message('{"success": true, "require_auth": true}')
        self.ip = self.request.remote_ip

    def on_message(self, message):
        raw = json.loads(message)

        if sql.Verify(raw["uuid"]):
            print(self.ip, "provided vaid uuid", raw["uuid"])
            id = sql.UuidToId(raw["uuid"])[0]
            cache.Update(id, raw["stats"])
            SendFetchMessage(raw)

        else:
            print(self.ip, "provided INVALID uuid", raw["uuid"])
            self.write_message('{"success":false,"errcode":"invalid_uuid"}')

    def on_close(self):
        id = sql.IpToId(self.request.remote_ip)[0]
        cache.TriggerOffline(str(id))


class FetchWebsocket(tornado.websocket.WebSocketHandler):

    def open(self):
        AliveSockets.add(self)
        print("Fetch websocket opened - client " + self.request.remote_ip)

    def on_message(self, message):
        print(self.request.remote_ip + " requested panel " + message)
        #res = scan.Fetch(message)
        res = "placeholder"
        self.write_message(res)
        print(self.request.remote_ip + " was sent " + message)

    def on_close(self):
        AliveSockets.remove(self)
        print("Fetch websocket closed - client " + self.request.remote_ip)


def SendFetchMessage(message):
    for ws in AliveSockets:
        ws.write_message(message)
