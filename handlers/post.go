package handlers

import (
	"io/ioutil"
	"log"
	"net/http"
)

type Post struct {
	Logger *log.Logger
}

func NewPost(logger *log.Logger) *Post {
	return &Post{logger}
}

func (post *Post) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK
	post.Logger.Println("Received request for 'POST'")
	// read json file from the request body
	data, _ := ioutil.ReadAll(r.Body)
	post.Logger.Println("File read: ", string(data))
}
