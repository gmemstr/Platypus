import tornado.ioloop
import tornado.web

from SQL import Sql

sql = Sql()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html", stats = sql.Get())

class ResourceHandler(tornado.web.RequestHandler):
    def get(self, resource):
            print(resource)
            res = open('webcontent/'+resource).read()
            self.set_header("Content-Type", 'text/css; charset="utf-8"')
            self.write(res)

def make_app():
    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/static/(.*)", ResourceHandler),
        ])

def run_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

run_app()