import tornado.ioloop
import tornado.web
import tornado.websocket
import socket
import ServerHandler
import Aor

sql = ServerHandler.Sql()
cache = ServerHandler.Cache()


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("i")


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/index.html",
                    servers=sql.Get(), stats=cache.Fetch())


class ResourceHandler(tornado.web.RequestHandler):

    def get(self, resource):
        print(resource)
        res = open('src/static/' + resource).read()
        self.set_header("Content-Type", 'text/css; charset="utf-8"')
        self.write(res)


class LoginManager(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/login.html")

    def post(self):
        self.set_secure_cookie("i", "TODO_RANDOM_KEY")
        self.redirect("/admin")


class AdminInterface(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("templates/admin.html", servers=sql.Get())

    @tornado.web.authenticated
    def delete(self):
        sql.Delete(self.get_body_argument("id"))
        self.write("success")

    @tornado.web.authenticated
    def post(self):
        ip = socket.gethostbyname(self.get_body_argument("hostname"))
        sql.New(self.get_body_argument("name"),
                self.get_body_argument("hostname"),
                ip)
        self.write("success")


def make_app():

    settings = {
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        "login_url": "/login",
        "xsrf_cookies": True,
        "debug": True
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/static/(.*)", ResourceHandler),
        (r"/fetch", Aor.FetchWebsocket),
        (r"/login", LoginManager),
        (r"/admin", AdminInterface),
        (r"/aor", Aor.AorMaster)
    ], **settings)


def run_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

run_app()
