package handlers

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

type Post struct {
	Logger *log.Logger
}

type Message struct {
	Message string `json:"message"`
}

func NewPost(logger *log.Logger) *Post {
	return &Post{logger}
}

func (post *Post) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) // 200 OK

	// open json file
	jsonFile, err := os.Open("message.json")
	if err != nil {
		post.Logger.Println(err)
		return
	}
	fmt.Println("Successfully Opened message.json")
	// defer the closing of our jsonFile
	defer jsonFile.Close()

	// read our opened jsonFile as a byte array.
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var message Message
	// we unmarshal our byteArray which contains our
	// jsonFile's content into 'users' which we defined above.
	json.Unmarshal(byteValue, &message)
	// we then print out the content of Message which is
	// a slice of type Message.
	post.Logger.Println(message.Message)
}

// // read message.json
// message, err := ioutil.ReadFile("message.json")
// if err != nil {
// 	post.Logger.Println(err)
// 	return
// }
// // parsing message.json
// err = json.Unmarshal(message, &message)
// if err != nil {
// 	post.Logger.Println(err)
// 	return
// }
