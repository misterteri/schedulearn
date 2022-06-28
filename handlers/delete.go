package handlers

import (
	"log"
	"net/http"
)

type Delete struct {
	Logger *log.Logger
}

func NewDelete(logger *log.Logger) *Delete {
	return &Delete{logger}
}

func (delete *Delete) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK
	w.Write([]byte("Received request for 'DELETE'\n"))
	delete.Logger.Println("Received request for 'DELETE'")
}
