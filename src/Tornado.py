import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import asyncio

from Scan import Scan
from SQL import Sql

sql = Sql()
scan = Scan()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html", stats = sql.Get())

class ResourceHandler(tornado.web.RequestHandler):
    def get(self, resource):
            print(resource)
            res = open('src/static/'+resource).read()
            self.set_header("Content-Type", 'text/css; charset="utf-8"')
            self.write(res)

class FetchWebsocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Fetch websocket opened - client " + self.request.remote_ip)

    def on_message(self, message):
        print(self.request.remote_ip + " requested panel " + message)
        res = scan.Fetch(message)
        self.write_message(res)

    def on_close(self):
        print("Fetch websocket closed")

def make_app():
    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/static/(.*)", ResourceHandler),
            (r"/fetch", FetchWebsocket)
        ])

def run_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

run_app()