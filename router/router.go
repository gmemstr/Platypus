package router

import (
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

type NewConfig struct {
	Name        string
	Host        string
	Email       string
	Description string
	Image       string
	PodcastURL  string
}

// Handle takes multiple Handler and executes them in a serial order starting from first to last.
// In case, Any middle ware returns an error, The error is logged to console and sent to the user, Middlewares further up in chain are not executed.
func Handle(handlers ...common.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		rc := &common.RouterContext{}
		for _, handler := range handlers {
			err := handler(rc, w, r)
			if err != nil {
				log.Printf("%v", err)

				w.Write([]byte(http.StatusText(err.StatusCode)))

				return
			}
		}
	})
}

func Init() *mux.Router {

	r := mux.NewRouter()

	// "Static" paths
	r.PathPrefix("/assets/").Handler(http.StripPrefix("/assets/", http.FileServer(http.Dir("web/assets"))))

	// Paths that require specific handlers
	r.Handle("/", Handle(
		rootHandler(),
	)).Methods("GET")

	return r
}

// Handles / endpoint
func rootHandler() common.Handler {
	return func(rc *common.RouterContext, w http.ResponseWriter, r *http.Request) *common.HTTPError {

		var file string
		switch r.URL.Path {
		case "/":
			w.Header().Set("Content-Type", "text/html")
			file = "web/index.html"
		default:
			return &common.HTTPError{
				Message:    fmt.Sprintf("%s: Not Found", r.URL.Path),
				StatusCode: http.StatusNotFound,
			}
		}

		return common.ReadAndServeFile(file, w)
	}
}

func adminHandler() common.Handler {
	return func(rc *common.RouterContext, w http.ResponseWriter, r *http.Request) *common.HTTPError {
		return common.ReadAndServeFile("web/admin.html", w)
	}
}
