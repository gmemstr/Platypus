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
	Ip string
	Stats UsageStats
}

var servers []Server
var upgrader = websocket.Upgrader{}

// Handles individual connections, parsing JSON data from client and writing a message.
func Handler() common.Handler {
	return func(rc *common.RouterContext, w http.ResponseWriter, r *http.Request) *common.HTTPError {
		c, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			panic(err)
		}
		defer c.Close()
		accept, err := ServerAuthHandler(c)
		if err != nil {
			panic(err)
		}
		if accept != true {
			_ = c.Close()
			return nil
		}
		c.SetCloseHandler(CloseHandler)

		for {
			mt, message, err := c.ReadMessage()
			if err != nil {
				break
			}
			stats := UsageStats{}
			err = json.Unmarshal(message, &stats)
			if err != nil {
				break
			}
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

func ServerAuthHandler(c *websocket.Conn) (bool, error) {
	for i := range servers {
		if servers[i].Ip == c.RemoteAddr().String() {
			return true, nil
		}
	}

	return true, nil
}

func WriteStats(ip string, stats UsageStats) error {
	create := true
	for i := range servers {
		if servers[i].Ip == ip {
			servers[i].Stats = stats
			create = false
		}
	}
	if create {
		servers = append(servers,  Server{
			Ip: ip,
			Stats: stats,
		})
	}

	jsonServers, err := json.Marshal(servers)
	if err != nil {
		return err
	}
	ioutil.WriteFile("stats.json", jsonServers, 0644)
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
