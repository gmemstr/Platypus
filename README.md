# Platypus
(new) Internal GGServers Status Page Flask Application

Scans servers and caches the results in a .json file that
is refreshed once the cache has aged 15 minutes or more.

### Current Features
 - Scan servers from .json list
 - Cache results along with time of scan 
 - Can filter by physical server location
 - Force rescan of all servers
 
### Planned Features
 - Sleeker webpage
 - Slack bot intergration
 - RESTful API
 - Dedicated configuration file
 - Docker image

## Requirements
 - Python 3.x
 - Flask 0.11.x
 - `requests` Python Library
 
## Running
`__init__.py` is where the magic happens. For testing, you can
do the following:

```
git clone git@github.com:GGServers/Platypus.git

cd Platypus/

export FLASK_APP=__init__.py

python -m flask run
```

## Configuration
Store all the servers you want to check the status of in `servers.json`.
The basic layout is like so:

```
[
	{
		"name" : "Panel 1",
		"hostname" : "first.gmem.pw",
		"location" : "MT"
	},
	{
		"name" : "Panel 2",
		"hostname" : "second.gmem.pw",
		"location" : "LA"
	}
]
```

 - `name`: What you want the server to show up as on the list
 - `hostname`: The location of your server. Can be IP or domain.
 - `location`: For geolocation filtering.
 
## Paths

| URL | What |
| --- | ---- |
| `/` | Main homepage, loads all servers |
| `/blob/<location>` | Displays servers from a specific location |
| `/forcescan` | Forces Python to scan all the servers again |