(This is my first attempt making a HACKME file so bear with me)

HACKME
===

## High Level File Structure Overview

    \ - platypus ; Main app directory
        \ - App.py ; Main app script
        \ - HACKME.md ; This file
        \ - LICENSE ; License file that you should obey
        \ - README.md ; README 
        \ - config.json ; Main config file for various options
        \ - requirements.txt ; pip requirements file
        \ - src ; Source code folder
            \ - Cache.py ; Handles JSON caching
            \ - Config.py ; Fetches and sets config.json properties
            \ - Slackbot.py ; Handles auto-posting to Slack
            \ - Statuses.py ; Scans each panel for stats
            \ - Webserver.py ; Runs the webserver (API/dash) frontend
            \ - Scripts ; Deployment scripts for your servers
                \ - php ; PHP script
                    \ - index.php ; Returns cpu/hdd/memory usages
                \ - python ; Python script
                    \ - Run.sh ; Auto-installs and starts Python webserver
                    \ - Stats.py ; Minimal Python webserver that returns stats
            \ - cache ; Cache folder 
                \ - servers.json ; List of servers to scan
                \ - stats.json ; Cache of server stats
            \ - static ; Static flask assets
                \ - Logo-02.png ; Logo 1
                \ - Logo-06.png ; Logo 2
                \ - index.css ; Main CSS file
                \ - platypus.js ; Primary JavaScript file
            \ - templates ; Templates library
                \ - index.html ; List jinja2 template

    