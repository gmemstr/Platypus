package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gmemstr/platypus/router"
	"github.com/gmemstr/platypus/stats"
)

func main() {
	go stats.Listener()
	r := router.Init()
	fmt.Println("Your Platytpus instance is live on port :3000")
	log.Fatal(http.ListenAndServe(":3000", r))
}
