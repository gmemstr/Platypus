package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gmemstr/platypus/router"
)

func main() {
	r := router.Init()
	fmt.Println("Your Platytpus instance is live on port :3000")
	log.Fatal(http.ListenAndServe(":3000", r))
}
