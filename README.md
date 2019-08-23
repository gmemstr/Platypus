# Platypus
## Simple realtime server monitoring

[![CircleCI](https://circleci.com/gh/gmemstr/Platypus.svg?style=svg)](https://circleci.com/gh/gmemstr/Platypus)
[![https://img.shields.io/badge/demo-status.gmem.ca-black.svg](https://img.shields.io/badge/demo-status.gmem.ca-black.svg?style=for-the-badge)](https://status.gmem.ca) 
[![https://img.shields.io/badge/frontend-gmemstr%2Fplatypus--react-blue.svg](https://img.shields.io/badge/frontend-gmemstr%2Fplatypus--react-blue.svg?style=for-the-badge)](https://github.com/gmemstr/platypus-react)

### Dependencies

```bash
go get github.com/gorilla/mux
go get github.com/gorilla/websocket
go get github.com/go-yaml/yaml
go get github.com/shirou/gopsutil
```

### Usage

Master server:
```bash
go build -o platypus main.go
chmod +x platypus
./platypus
```

Client servers:
```bash
go build -o platypus_client client/client.go
chmod +x platypus_client
nano config.yml
# Input your secret key and master server IP here, secret key found on master server in .secret
# master: example.com
# secret: s3cr3tk3y
# End config
./platypus_client
```

Navigate to your master server and check out the stats.

## Rewrite 

Rewriting this from the ground up. Why did I do this in Python.

The goal of the rewrite is to move away from using Python for the entire stack 
and instead break things up into smaller chunks, maybe moving this to it's own
GitHub / Gitlab org, which will allow it to be much more modular and open ended
when it comes to what kind of information you want to monitor and how.

### Steps

1. Rewriting the core functionality, which is a basic stats dashboard
and server management through an admin interface. We also want to rethink how to
handle Active Online Reporting - websockets still _seems_ like the best option
for this but there's got to be a better way. Might opt for Go master server
side as it's something I have experience in and should offer good performance etc.

2. Rebuild the client based on the specifications of #1, and deciding the best
way to build and distribute the package w/ configuration - I personally want to
go with something we can compile into a very small package and ship with a
master server-generated configuration file of some sort. Was thinking C++ might
be a good option over Go size wise but there could be additional time overhead.

3. Write a straightforward API both client (or "node") side, which would allow
applications to construct and send custom messages to the master server, and
master server side, which will handle said customer messages. This should be fairly
straightforward once we have #1 and #2 complete.

4. A plugin system - I don't really know what form this would take since it's pretty
far down the line, but it's something to consider. Some sort of simple scripting
language that we can easily write an interpreter for in Go for the master server and
would expose various variables / functions.

