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

	// read message.json
	message, err := ioutil.ReadFile("message.json")
	if err != nil {
		post.Logger.Println(err)
		return
	}

	// write the body of the message to the log
	post.Logger.Println("File read: ", string(message))
}
