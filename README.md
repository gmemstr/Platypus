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

## Getting Started

Please see the wiki page [Getting Started](https://github.com/gmemstr/Platypus/wiki/Getting-Started)

## Requirements
 - Python 3.x (2.x not officially supported)
 - pip
  - `pip install -r requirements.txt`
 - MariaDB or MySQL

## Running
See [Getting Started](https://github.com/gmmemstr/Platypus/wiki/Getting-Started)

## Script

Included in the `Scripts` folder is the node-side `aor.py` script. This should be
deployed to the machines you would like to monitor, and modified to point towards
your master server. There is also a `Dockerfile` available, again you will need to modify the config (`aor_config.json`) before building (just fill out the master key and master host). You can also feel free to use your own custom script, however it has to be fully websocket compatible. See below about the data passed to the master.

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

Edit `aor_config.json` then build the image as you normally would.
