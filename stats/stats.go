package stats

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gmemstr/platypus/common"
	"github.com/gorilla/websocket"
	"io"
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
var r, w = io.Pipe()
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
	buf := new(bytes.Buffer)
	_, err := buf.ReadFrom(r)
	if err != nil {
		return false, err
	}
	var serverList []Server
	err = json.Unmarshal(buf.Bytes(), &serverList)
	if err != nil {
		return false, err
	}
	for i := range serverList {
		if serverList[i].Ip == c.RemoteAddr().String() {
			return true, nil
		}
	}

	return true, nil
}

func WriteStats(ip string, stats UsageStats) error {
	serverList, err := ReadStats()
	if err != nil {
		return err
	}

	for i := range serverList {
		if serverList[i].Ip == ip {
			serverList[i].Stats = stats
		}
	}

	jsonServers, err := json.Marshal(serverList)

	_, err = fmt.Fprint(w, jsonServers)
	if err != nil {
		return err
	}
	w.Close()
	return nil
}

func ReadStats() ([]Server, error) {
	buf := new(bytes.Buffer)
	_, err := buf.ReadFrom(r)
	if err != nil {
		return servers, err
	}
	err = json.Unmarshal(buf.Bytes(), &servers)
	if err != nil {
		return servers, err
	}
	return servers, nil
}

// Close handler, begin chain of escalation.
func CloseHandler(code int, text string) error {
	if code != 1000 {
		return errors.New("websocket closed badly")
	}
	return nil
}
