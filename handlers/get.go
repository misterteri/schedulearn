package handlers

import (
	"log"
	"net/http"
)

type Get struct {
	Logger *log.Logger
}

func NewGet(logger *log.Logger) *Get {
	return &Get{logger}
}

func (get *Get) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK
	w.Write([]byte("Received request for 'GET'\n"))
	get.Logger.Println("Received request for 'GET'")
}