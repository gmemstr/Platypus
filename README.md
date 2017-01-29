# Platypus
(new) Internal GGServers Status Page Flask Application

Scans servers and caches the results in a .json file including
server usage stats if available. Provides webpage frontend, raw
json access and basic slackbot for monitoring results.

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
 - pip
  - `pip install -r requirements.txt`

## Running
`App.py` is the primary Python file for running the project. It's
as simple as:

```
git clone https://github.com/ggservers/Platypus

cd Platypus

pip install -r requirements.txt

python App.py
```

The server will then be running on `127.0.0.1:8080`. You will
need to populate `src/cache/servers.json` with your own list of
servers (described below).

## Configuration

### Master Server


### Servers
Store all the servers you want to check the status of in `servers.json`.
The basic layout is like so:

```
[
	{
		"id": 0,
		"name" : "First Subdomain",
		"hostname" : "first.gmem.pw",
		"location" : "Global"
	},
	{
		"id", 1,
		"name" : "Second Subdomain",
		"hostname" : "second.gmem.pw",
		"location" : "LA"
	}
]
```
 - `id`: Unique int for your server, preferably in ascending order. 
 - `name`: What you want the server to show up as on the list
 - `hostname`: The location of your server. Can be IP or domain.
   - Path to custom script will be automatically added, see #Script
 - `location`: For geolocation filtering.

## Script

Included in this repo is a custom script written in various
languages that Platypus will attempt to fetch for the various
server stats (memory, CPU and disk usage). It is written in
Python and PHP, and you can choose whichever one you feel like
using - Platypus does not care which version you use, and will
still check if your server is offline if it results in a 404.

### Using Python

Just copy the `Scripts/python/` folder to your servers. Next, you'll need to
[set up a proxy with nginx](#) that will point towards `127.0.0.1:9000` using
the path `<server URL>/platy/` (e.g `first.gmem.pw/platy/`). Finally,
you can go back to the `Scripts/python/` folder and run `Run.sh` (you will
require `screen`). It will handle everything. If you choose to visit the URL
for the stats, you will find some json displaying various info about your
server. This data is fetched on request.

### Using PHP

Copy over the contents of `Scripts/php/` to your server directory under a
directory named `platy/` wherever your webserver files are served from.
You will require the latest version of PHP and a webserver installed
(e.g Apache or nginx).


## Paths

| URL | What |
| --- | ---- |
| `/` | Main homepage, loads all servers |
| `/raw/<file>` | Returns raw cache data from `<file>` |