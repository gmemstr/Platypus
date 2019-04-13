package stats

import (
	"encoding/json"
	"errors"
	"github.com/gmemstr/platypus/common"
	"github.com/gorilla/websocket"
	"io/ioutil"
	"net/http"
)

type UsageStats struct {
	Cpu    float64 `json:"cpu"`
	Memory float64 `json:"memory"`
	Disk   float64 `json:"disk"`
	Secret string  `json:"secret"`
}

type Server struct {
	Ip string `json:"ip"`
	Stats UsageStats `json:"stats"`
	Online bool `json:"online"`
}

var Servers []Server
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// Handles individual connections, parsing JSON data from client and writing a message.
func Handler() common.Handler {
	return func(rc *common.RouterContext, w http.ResponseWriter, r *http.Request) *common.HTTPError {
		c, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			panic(err)
		}
		defer c.Close()
		c.SetCloseHandler(CloseHandler)

		for {
			mt, message, err := c.ReadMessage()
			if err != nil {
				_ = SetOffline(c.RemoteAddr().String())
				break
			}
			stats := UsageStats{}
			err = json.Unmarshal(message, &stats)
			if err != nil {
				break
			}
			secretKey, err := ioutil.ReadFile(".secret")
			key := string(secretKey)
			if stats.Secret != key {
				_ = c.WriteMessage(mt, []byte("invalid secret key"))
				_ = c.Close()
			}
			// Blank out secret key after comparing.
			stats.Secret = ""
			err = WriteStats(c.RemoteAddr().String(), stats)
			if err != nil {
				break
			}
			err = c.WriteMessage(mt, []byte(""))
			if err != nil {
				break
			}
		}

		return nil
	}
}

func SetOffline(ip string) error {
	for i := range Servers {
		if Servers[i].Ip == ip {
			Servers[i].Online = false
		}
	}

	jsonServers, err := json.MarshalIndent(Servers, "", "  ")
	if err != nil {
		return err
	}
	err = ioutil.WriteFile("stats.json", jsonServers, 0644)
	if err != nil {
		return err
	}

	return nil
}

func WriteStats(ip string, stats UsageStats) error {
	create := true
	for i := range Servers {
		if Servers[i].Ip == ip {
			Servers[i].Stats = stats
			Servers[i].Online = true
			create = false
		}
	}
	if create {
		Servers = append(Servers,  Server{
			Ip: ip,
			Stats: stats,
			Online: true,
		})
	}

	jsonServers, err := json.MarshalIndent(Servers, "", "  ")
	if err != nil {
		return err
	}
	err = ioutil.WriteFile("stats.json", jsonServers, 0644)
	if err != nil {
		return err
	}

	return nil
}

// Close handler, begin chain of escalation.
func CloseHandler(code int, text string) error {
	if code != 1000 {
		return errors.New("websocket closed badly")
	}
	return nil
}
