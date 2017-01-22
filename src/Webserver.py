# Python modules
from flask import Flask, render_template, send_from_directory, jsonify
import time
import threading

# Custom imports
from src.Cache import Fetch


app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html",
                           stats=sorted(Fetch("stats", False).items(),
                                        key=lambda i: int(i[0])))


@app.route('/raw')
def ReturnRawStats():
    file = open("src/cache/stats.json", "r").read()
    return file

class Webserver:
    def Run(self):
        app.run(port=8080)  # Run server on port 8080
        # Internally this webserver is proxied through nginx,
        # so we don't really worry about setting what
        # IP to run the webserver on.
