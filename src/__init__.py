from flask import Flask, render_template
import Scan
from os import environ
app = Flask(__name__)

@app.route('/')
def checkall():
	return render_template("list.html", location = "worldwide", downs = Scan.cache("all"))
	
@app.route('/blob/<lctn>')
def checkone(lctn):
	return render_template("list.html", location = lctn, downs = Scan.cache(lctn))

@app.route('/forcescan')
def forcescan():
	Scan.updatecache()
	return "<script>window.location.href = '/';</script>"
	
if __name__ == '__main__':
	app.run()
   # app.run(host='0.0.0.0') # Make server purblicly visible