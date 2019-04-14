package main

import (
	"encoding/json"
	"github.com/go-yaml/yaml"
	"github.com/gorilla/websocket"
	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/disk"
	"github.com/shirou/gopsutil/mem"
	"io/ioutil"
	"log"
	"net/url"
	"os"
	"os/signal"
	"time"
)

type UsageStats struct {
	Hostname string  `json:"hostname"`
	Cpu      float64 `json:"cpu"`
	Memory   float64 `json:"memory"`
	Disk     float64 `json:"disk"`
	Secret   string  `json:"secret"`
}

type Configuration struct {
	Master string `yaml:"master"`
	Secret string `yaml:"secret"`
}

func main() {
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	conf := Configuration{}
	file, err := ioutil.ReadFile("config.yml")
	if err != nil {
		panic(err)
	}
	err = yaml.Unmarshal(file, &conf)
	if err != nil {
		panic(err)
	}

	if err != nil {
		panic(err)
	}

	addr := conf.Master
	u := url.URL{Scheme: "ws", Host: addr, Path: "/stats"}
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		panic(err)
	}
	defer c.Close()

	done := make(chan struct{})
	go func() {
		defer close(done)
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				break
			}
			log.Printf("recv: %v", message)
		}
	}()

	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-done:
			return
		case <-ticker.C:
			stats, err := GetStats()
			if err != nil {
				break
			}
			stats.Secret = conf.Secret
			statsJson, err := json.Marshal(stats)
			if err != nil {
				break
			}
			err = c.WriteMessage(websocket.TextMessage, statsJson)
			if err != nil {
				log.Println("write:", err)
				return
			}
		case <-interrupt:
			log.Println("interrupt")

			// Cleanly close the connection by sending a close message and then
			// waiting (with timeout) for the server to close the connection.
			err := c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
			if err != nil {
				log.Println("write close:", err)
				return
			}
			select {
			case <-done:
			case <-time.After(time.Second):
			}
			return
		}
	}
}

// Fetch usage stats using gopsutil.
func GetStats() (UsageStats, error) {
	stats := UsageStats{
	}
	diskUsage, err := disk.Usage("/")
	if err != nil {
		return stats, err
	}
	stats.Disk = diskUsage.UsedPercent

	cpuUsage, err := cpu.Percent(0, false)
	if err != nil {
		return stats, err
	}
	stats.Cpu = cpuUsage[0]

	memUsage, err := mem.VirtualMemory()
	if err != nil {
		return stats, err
	}
	stats.Memory = memUsage.UsedPercent

	hostname, err := os.Hostname()
	if err != nil {
		return stats, err
	}
	stats.Hostname = hostname
	return stats, nil
}
