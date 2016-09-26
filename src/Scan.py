import requests
import json
import time

def servers():
	file = open("servers.json", "r").read()
	servers_list = json.loads(file)
	
	return servers_list
	
def check(lctn):
	servers_downlist = [
	]
	
	servers_targets = servers()
	
	for server in servers_targets:
		if server["location"] == lctn.upper() or lctn.upper() == "ALL":
			print("scanning " + server["name"], end="")
			try:
				req = requests.get("http://" + server["hostname"], timeout = 0.6)
				print(" - responding")
			except:
				print(" - unresponsive")
				servers_downlist.append({ "name": server["name"], "location": server["location"] })
			
	return servers_downlist

def cache(lctn):
	result = []
	file = open("cache.json", "r")
	cachejson = json.load(file)
	
	if time.time() - cachejson["time"] >= 900:
		print("updating cache")
		cachejson = json.loads(updatecache())
	else:
		print("cache up to date (<15 min old)")

	for server in cachejson["servers"]:
		if server["location"] == lctn.upper() or lctn.upper() == "ALL":
			result.append(server["name"])
		
	return result
		
def updatecache():
		data = {
			"time":time.time(),
			"servers":check("all") 
		}
		file = open("cache.json", "w")
		json.dump(data, file)
		
		return json.dumps(data)