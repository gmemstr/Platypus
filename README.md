# Platypus
(new) Internal GGServers Status Page Flask Application

Scans servers and caches the results in a .json file that
is refreshed once the cache has aged 15 minutes or more.

### Current Features
 - Scan servers from .json list
 - Can filter by physical server location
 - Fetch server stats based on script
- (Optional) Log server stats per-day

### Planned Features
 - Sleeker webpage
 - Slack bot intergration
 - RESTful API for scanning / fetching results nicely

## Requirements
 - Python 3.x
 - Flask 0.11.x
 - `requests` Python Library

 (See `requirements.txt` or run `pip install -r requirements.txt`)

## Running
`Webserver.py` is the primary Python file for running the project. It's
as simple as:

```
git clone https://github.com/ggservers/Platypus

cd Platypus

pip install -r requirements.txt

python Webserver.py
```

The server will then be running on `127.0.0.1:8080`. You will
need to populate `src/json/servers.json` with your own list of
servers (described below).

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
   - Include a unique int ID in the name for sorting / filtering
 - `hostname`: The location of your server. Can be IP or domain.
   - Path to custom script will be automatically added, see #Script
 - `location`: For geolocation filtering.

## Script

Included in this repo is a custom script written in various
languages that Platypus will attempt to fetch for the various
server stats (memory, CPU and disk usage). It is written in
Python and PHP, and you can choose whichever one you feel like
using - Platypus will attempt to discover which version you have
used.

### Using Python

Just copy the `Scripts/python/` folder to your servers. Next, you'll need to
[set up a proxy with nginx](#) that will point towards `127.0.0.1:9000` using
the path `<server URL>/platy/` (e.g `first.gmem.pw/platy/`). Finally,
you can go back to the `Scripts/python/` folder and run `Run.sh` (you will
require `screen`). It will handle everything. If you choose to visit the URL
for the stats, you will find some json displaying various info about your
server.

### Using PHP

Copy over the contents of `Scripts/php/` to your server directory under a
directory named `platy/` wherever your webserver files are served from.
You will require the latest version of PHP and a webserver installed
(e.g Apache or nginx).


## Paths

| URL | What |
| --- | ---- |
| `/` | Main homepage, loads all servers |
| `/raw` | Returns raw cache data from `src/json/stats.json` |