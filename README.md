# Platypus

[Live Master Branch](https://status.ggserv.xyz)

Scaleable Server Infrastructure Monitoring Python App

(Probably Light and Technically Pretty Unassuming Software)

Even More Buzzwords For SEO Reasons

Monitors and reports statistics of your server infrastucture, including usage statistics, uptime, downtime, etc.

### Current Features
 - Setup script
 - Scan servers from a SQL database
 - Log scan results to database
 - Auto-update uptime or downtime
 - Auto-post to Slack with scan results
 - Fetch and save server usage statistics
 - Provide live server usage statistics with web frontend
 - Simple JSON API for building apps

### Planned Features
 - Cleaner code
 - Smaller resource footprint
 - More advanced scanning method

## Requirements
 - Python 3.x (2.x not officially supported)
 - pip
  - `pip install -r requirements.txt`
 - MariaDB

## Running
Run `python setup.py` to set up your instance, including creating the MariaDB databse and setting an admin password.

Finally you can run `python App.py` and go navigate to `127.0.0.1:8080/login` to get to the admin control panel.

To expose it to the world, I recommend using an [nginx proxy](https://www.nginx.com/resources/admin-guide/reverse-proxy/).
## Configuration

```
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
    "admin_password": "$2b$12$q1oiev5KEoOPvWJe7b5xuOm3PU61Ks9c2Y9e4ZFzS1YzJtsFLBBBK", // Admin password (salted & hashed) 
    "sql_user":"root", // MariaDB Username
    "sql_host":"localhost", // DB Host
    "sql_pass": "", // DB Password
    "sql_db": "server" // DB Table
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
 - Install Python 3
 - `pip install psutil`
 - Move `Stats.py` to your server
 - `chmod +x Stats.py`
 - `screen ./Stats.py`
(Screen is recommended)
 - [Set up a proxy with nginx](https://www.nginx.com/resources/admin-guide/reverse-proxy/)

### Using PHP
 - Move `index.php` to whever your web files are
  - Feel free to rename `index.php` and put it wherever
 - Visit the path that corresponds with where you put it

### Returned data
 - Used CPU
 - Used memory
 - Used disk space

 `{"cpu": 6, "memory": 38, "disk": 8}`

Some stats may vary slightly between script, this is simply due to the methods used to get
the statistics.

## Paths

| URL | What | Method |
| --- | ---- | ---- |
| `/` | Main homepage, loads all servers | `GET` |
| `/raw` | Returns raw cache data | `GET` |
| `/fetch/<panel>` | Get server usage stats live (CORS middleman) | `GET` |
| `/login` | Login page or POST route | `GET`, `POST` |
| `/admin` | Admin management page | `GET` (requires admin cookie) |
| `/ac/remove/<panel>` | Admin route for removing server. | `DELETE` (requires admin cookie) |
| `/ac/new` | Create new server in database | `POST` |