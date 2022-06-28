package handlers

import (
	"log"
	"net/http"
)

type Post struct {
	Logger *log.Logger
}

func NewPost(logger *log.Logger) *Get {
	return &Get{logger}
}

func (post *Post) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK
	w.Write([]byte("Received request for 'POST'\n"))
	post.Logger.Println("Received request for 'POST'")
}