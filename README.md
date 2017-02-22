# Platypus

[Live Master Branch](https://status.ggserv.xyz)

Scaleable Server Infrastructure Monitoring Python App
(Probably Light and Technically Pretty Unassuming Software)
Even More Buzzwords For SEO Reasons

Monitors and reports statistics of your server infrastucture, including usage statistics, uptime, downtime, etc.

### Current Features
 - Scan servers from a SQL database
 - Log scan results to database
 - Auto-update uptime or downtime
 - Auto-post to Slack with scan results
 - Fetch and save server usage statistics
 - Provide live server usage statistics with web frontend
 - Simple JSON API for building apps

### Planned Features
 - Cleaner code
 - Autoinstaller script
 - Smaller resource footprint
 - More advanced scanning method

## Requirements
 - Python 3.x (2.x not officially supported)
 - pip
  - `pip install -r requirements.txt`
 - MySQL / MariaDB

## Running
You'll want to first set up your SQL database - a skeleton file you can import is located in the `Scripts` folder. Else see the SQL database specifications.

_Currently_ you'll want to go through and tweak all the values in `config.json` to the values you want/need. Run `python src/Login.py` to generate a new admin password (the default is `p1atyPus`, PLEASE CHANGE IT IN PRODUCTION).

Finally you can run `python App.py` and go from there.

To expose it to the world, I recommend using an [nginx proxy](#).
## Configuration

```json
{
    "comments": [
        "This is the config file for Platypus.",
        "These comments are ignored. If you need",
        "any guidance see the README",
        "Default password is p1atyPus, run python src/Login.py to",
        "generate a new one."
    ],
    "enable_slackbot": false, // Slackbot intergration
    "enable_webserver": true, // Webserver toggle
    "webserver_port": 8080, // Webserver port
    "slack_api_key": "", // Slack API key 
    "slack_channel": "", // Channel you'd like to post to
    "slack_interval": 3600, // Seconds between Slack post
    "scan_interval": 300, // Seconds betweeen scan
    "scan_timeout": 5, // Seconds before connection times out
    				   // More accurate = higher, faster = lower
    "stats_path": "/status/platypus.php", // Location of status script
    "admin_username": "admin", // Admin username
    "admin_password": "$2b$12$q1oiev5KEoOPvWJe7b5xuOm3PU61Ks9c2Y9e4ZFzS1YzJtsFLBBBK" // Admin password (salted & hashed) 
}
```

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

| URL | What | Method |
| --- | ---- | ---- |
| `/` | Main homepage, loads all servers | `GET` |
| `/raw` | Returns raw cache data | `GET` |
| `/fetch/<panel>` | Get server usage stats live (CORS middleman) |
| `/login` | Login page or POST route | `GET`, `POST` |
| `/admin` | Admin management page | `GET` (requires admin cookie) |
| `/ac/<panel>` | Admin control route, takes many methods for various actions. | `DELETE`, `PUT`, `POST`, `GET` (requires admin cookie) |