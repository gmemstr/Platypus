# Python modules
from flask import Flask, render_template, abort, g, request, redirect, url_for

# Custom imports
from src.Login import LoginManager, User
from src.Cache import Fetch
from src.Config import Config

lm = LoginManager()
user = User()
config = Config()

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template("index.html",
                           stats=Fetch("stats", False).items())


# @TODO: Make it impossible to get at config.json
@app.route('/raw/<filename>')
def ReturnRawStats(filename):
    try:
        file = open("src/cache/"+filename+".json", "r").read()
        return file
    except:
        abort(404)

# TODO: Finish login!
@app.route("/login", methods=["GET", "POST"])
def LoginRoute():
    if request.method == 'POST':
        uid = lm.Login(request.form["username"], request.form["password"])
        if uid == False:
            return redirect(url_for('LoginRoute', next=url_for("AdminInterface")))
        else:
            redirect_to_index = redirect('/admin')
            response = app.make_response(redirect_to_index )  
            response.set_cookie('uid',value=uid)
            user.UserID(uid)
            return response
    else:
        return render_template("login.html")

@app.route("/admin")
def AdminInterface():
    cuid = request.cookies.get('uid')
    if user.UserID(cuid):
        return render_template("admin.html", 
                                servers=Fetch("servers", False),
                                configs=config.Get("*"))
    else:
        return redirect(url_for('LoginRoute', next=url_for("AdminInterface")))

class Webserver:
    def Run(self):
        app.run(port=config.Get("webserver_port"))
        # Internally this webserver is proxied through nginx,
        # so we don't really worry about setting what
        # IP to run the webserver on.
