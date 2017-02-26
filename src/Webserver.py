# Python modules
from flask import Flask, render_template, abort, g, request, redirect, url_for, jsonify
import requests

# Custom imports
from src.Login import LoginManager, User
from src.Cache import Handler
from src.Config import Config
from src.Statuses import Scanning

lm = LoginManager()
user = User()
config = Config()
handler = Handler()
scan = Scanning()

app = Flask(__name__)

@app.route('/')
def Index():
    return render_template("index.html",
                           stats=handler.Get())

@app.route('/raw')
def ReturnRawStats():
    res =  handler.GetAsJson()
    return jsonify(res)

@app.route('/fetch/<panel>')
def MiddlemanStat(panel):
    # Acts as a middleman for CORS reasons
    res = scan.Fetch(panel)
    return jsonify(res)

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
            user.UserID(uid, True)
            return response
    else:
        return render_template("login.html")

@app.route("/admin")
def AdminInterface():
    cuid = request.cookies.get('uid')
    if user.UserID(cuid):
        return render_template("admin.html", 
                                servers=handler.Get())
    else:
        return redirect(url_for('LoginRoute', next=url_for("AdminInterface")))

@app.route("/ac/remove/<panelid>", methods=["DELETE"])
def DelPanel(panelid):
    if panelid is None:
        abort(404)
    cuid = request.cookies.get('uid')
    if user.UserID(cuid,set=False):
        handler.RemoveServer(panelid)
        return "Panel " + str(panelid) + " deleted"
    else:
        abort(403)

@app.route("/ac/new", methods=["POST"])
def NewPanel():
    cuid = request.cookies.get('uid')
    if user.UserID(cuid,set=False):
        handler.CreateServer(request.form["id"],request.form)
        return "Panel created"
    else:
        abort(403)



class Webserver:
    def Run(self):
        app.run(port=config.Get("webserver_port"))
        # Internally this webserver is proxied through nginx,
        # so we don't really worry about setting what
        # IP to run the webserver on.
