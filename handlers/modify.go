package handlers

import (
	"log"
	"net/http"
)

type Modify struct {
	Logger *log.Logger
}

func NewModify(logger *log.Logger) *Modify {
	return &Modify{logger}
}

func (modify *Modify) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK
	w.Write([]byte("Received request for 'POST'\n"))
	modify.Logger.Println("Received request for 'POST'")
}