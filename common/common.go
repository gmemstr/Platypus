package common

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
)

// RouterContext contains any information to be shared with middlewares.
type RouterContext struct{}

// Handler is the signature of HTTP Handler that is passed to Handle function
type Handler func(rc *RouterContext, w http.ResponseWriter, r *http.Request) *HTTPError

type HTTPError struct {
	// Message to log in console
	Message string
	// Status code that'll be sent in response
	StatusCode int
}

type Configuration struct {
	Port     int `yaml:"port"`
	Interval int `yaml:"interval"`
}

var Config Configuration

// ReadAndServeFile reads the file from specified location and sends it in response
func ReadAndServeFile(name string, w http.ResponseWriter) *HTTPError {
	f, err := os.Open(name)
	if err != nil {

		if os.IsNotExist(err) {
			return &HTTPError{
				Message:    fmt.Sprintf("%s not found", name),
				StatusCode: http.StatusNotFound,
			}
		}

		return &HTTPError{
			Message:    fmt.Sprintf("error in reading %s: %v\n", name, err),
			StatusCode: http.StatusInternalServerError,
		}
	}

	defer f.Close()
	stats, err := f.Stat()
	if err != nil {
		log.Printf("error in fetching %s's  stats: %v\n", name, err)
	} else {
		w.Header().Add("Content-Length", strconv.FormatInt(stats.Size(), 10))
	}

	_, err = io.Copy(w, f)
	if err != nil {
		log.Printf("error in copying %s to response: %v\n", name, err)
	}
	return nil
}
