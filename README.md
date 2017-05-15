 ![https://img.shields.io/badge/Status-v3.0%20In%20Progress-green.svg](https://img.shields.io/badge/Status-v3.0%20In%20Progress-green.svg)

# Platypus

[Live Stable Branch](https://status.ggserv.xyz)

Active online and usage monitor using websockets and Python


## Features
 - Setup script
 - Websocket-based uptime monitoring (**AOR**)
 - Auto-post to Slack when server goes offline
 - Provide live server usage statistics with web frontend
 - Simple JSON API for building apps
 - Admin interface for managing servers

## Requirements
 - Python 3.x (2.x not officially supported)
 - pip
  - `pip install -r requirements.txt`
 - MariaDB or MySQL

## Running
Run `python setup.py` to set up your instance, including creating the databse and setting an admin password.

Finally you can run `python App.py` and go navigate to `127.0.0.1:8080/login` to get to the admin control panel.

To expose it to the world, I recommend using an [nginx proxy](https://www.nginx.com/resources/admin-guide/reverse-proxy/).
## Configuration

| Key | Default Value | What is |
| --- | ------------- | ------- |
| enable_slackbot | false | Enable automated Slack reports |
| enable_webserver | true | Enable web frontend and API | 
| webserver_port | 8080 | Port for webserver to run on |
| slack_api_key | | [API key for Slack posting](https://github.com/slackapi/python-slackclient)
| admin_username | admin | Username for admin interface |
| admin_password | | Password for admin interface |
| sql_user | root | SQL database username |
| sql_pass | | SQL database password |
| sql_host | localhost | SQL database host |
| sql_db | server | SQL data table |

## Script

Included in the `Scripts` folder is the node-side `aor.py` script. This should be
deployed to the machines you would like to monitor, and modified to point towards
your master server. A docker image is available _soon_ if you would prefer to 
use that. You can also feel free to use your own custom script, however it has to
be fully websocket compatible. See below about the data passed to the master.

### Requirements:

 - Python 3.x
 - websocket
 - psutil

`pip install websocket psutil`

### Deploying (Script)

You'll need Python 3.x installed on your nodes. Deploy `aor.py` and `aor_config.json`. You'll also want to change some values in the config file
to point towards the master, along with the master key. Your node with auto-authenticate
with the master.


### Deploying (Docker)

Coming soon