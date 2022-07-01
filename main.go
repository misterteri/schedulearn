package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"schedulearn/handlers"
	"syscall"
	"time"
)

func main() {
	logger := log.New(os.Stdout, "schedulearn ", log.LstdFlags)

	serveMux := http.NewServeMux()
	serveMux.Handle("/post", handlers.NewPost(logger))
	serveMux.Handle("/get", handlers.NewGet(logger))
	serveMux.Handle("/delete", handlers.NewDelete(logger))

	server := &http.Server{
		Handler:      serveMux,
		Addr:         ":8080",
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	go func() {
		err := server.ListenAndServe()
		if err != nil {
			logger.Fatal(err)
		}
	}() // run in background
	logger.Println("API up and running")

	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, os.Interrupt, syscall.SIGTERM)

	signal := <-signalChannel
	logger.Println("Received termination, gracefully shutdown", signal)

	tc, _ := context.WithDeadline(context.Background(), time.Now().Add(30*time.Second))
	server.Shutdown(tc)
}
