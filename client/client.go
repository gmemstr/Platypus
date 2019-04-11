package main

import (
	"github.com/go-yaml/yaml"
	"io/ioutil"
)

type UsageStats struct {
	Cpu float32 `json:"cpu"`
	Memory float32 `json:"memory"`
	Disk float32 `json:"disk"`
	Secret string `json:"secret"`
}

type ResponseMessage struct {
	Code string `json:"code"`
	Message string `json:"message"`
}

type Configuration struct {
	Master string `yaml:"master"`
	Secret string `yaml:"secret"`
}

func main() {
	conf := Configuration{}
	file, err := ioutil.ReadFile("config.yml")
	if err != nil {
		panic(err)
	}
	err = yaml.Unmarshal(file, &conf)
	if err != nil {
		panic(err)
	}
}