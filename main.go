package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/gmemstr/platypus/stats"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gmemstr/platypus/router"
)

func main() {
	if _, err := os.Stat(".secret"); os.IsNotExist(err) {
		fmt.Println("Generating secret key to .secret, use this to configure your servers")
		SecretKey()
	}
	if _, err := os.Stat("stats.json"); os.IsNotExist(err) {
		err = ioutil.WriteFile("stats.json", []byte("{}"), 0644)
		if err != nil {
			panic(err)
		}
	}
	// Repopulate servers from cache file.
	statsCache, err := ioutil.ReadFile("stats.json")
	if err != nil {
		panic(err)
	}
	err = json.Unmarshal(statsCache, &stats.Servers)
	if err != nil {
		panic(err)
	}
	// Cache server stats in event master goes down.
	defer func() {
		jsonServers, err := json.MarshalIndent(stats.Servers, "", "  ")
		if err != nil {
			panic(err)
		}
		err = ioutil.WriteFile("stats.json", jsonServers, 0644)
		if err != nil {
			panic(err)
		}
	}()


	// Start up server.
	r := router.Init()
	fmt.Println("Your Platytpus instance is live on port :3000")
	log.Fatal(http.ListenAndServe(":3000", r))
}

func SecretKey() {
	key, err := GenerateRandomString(32)
	if err != nil {
		panic(err)
	}
	err = ioutil.WriteFile(".secret", []byte(key), 0644)
	if err != nil {
		panic(err)
	}
}

// From https://stackoverflow.com/questions/32349807/how-can-i-generate-a-random-int-using-the-crypto-rand-package
func GenerateRandomBytes(n int) ([]byte, error) {
	b := make([]byte, n)
	_, err := rand.Read(b)
	// Note that err == nil only if we read len(b) bytes.
	if err != nil {
		return nil, err
	}

	return b, nil
}

// GenerateRandomString returns a URL-safe, base64 encoded
// securely generated random string.
func GenerateRandomString(s int) (string, error) {
	b, err := GenerateRandomBytes(s)
	return hex.EncodeToString(b), err
}
