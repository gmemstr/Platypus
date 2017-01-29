# Python modules
from flask import Flask, render_template, abort

# Custom imports
from src.Cache import Fetch


app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html",
                           stats=Fetch("stats", False).items())


@app.route('/raw/<filename>')
def ReturnRawStats(filename):
    try:
        file = open("src/cache/"+filename+".json", "r").read()
        return file
    except:
        abort(404)

class Webserver:
    def Run(self):
        app.run(port=8080)  # Run server on port 8080
        # Internally this webserver is proxied through nginx,
        # so we don't really worry about setting what
        # IP to run the webserver on.
