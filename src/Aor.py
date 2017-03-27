import tornado.ioloop
import tornado.websocket
import json
import ServerHandler

sql = ServerHandler.Sql()
cache = ServerHandler.Cache()

class AorMaster(tornado.websocket.WebSocketHandler):
    def open(self):
        print(self.request.remote_ip + " connected, asking for authentication...")
        self.write_message('{"success": true, "require_auth": true}')
        self.ip = self.request.remote_ip

    def on_message(self, message):
        raw = json.loads(message)

        if sql.Verify(raw["uuid"]):
        	id = sql.UuidToId(raw["uuid"])
        	cache.Update(id,raw["stats"])

        else:
        	self.write_message('{"success":false,"errcode":"invalid_uuid"}')

	def on_close(self):
		id = sql.IpToId(self.ip)
		cache.TriggerOffline(id)