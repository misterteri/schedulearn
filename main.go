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
	serveMux.Handle("/api/v1/post/", handlers.NewPost(logger))
	serveMux.Handle("/api/v1/get/", handlers.NewGet(logger))
	serveMux.Handle("/api/v1/delete/", handlers.NewDelete(logger))

	server := &http.Server{
		Addr:         ":8080",
		Handler:      serveMux,
		IdleTimeout:  120 * time.Second,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 5 * time.Second,
	}

	go func() {
		err := server.ListenAndServe()
		if err != nil {
			logger.Fatal(err)
		}
	}() // run in background

	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, os.Interrupt, syscall.SIGTERM)

	signal := <-signalChannel
	logger.Println("Received termination, gracefully shutdown", signal)

	tc, _ := context.WithDeadline(context.Background(), time.Now().Add(30*time.Second))
	server.Shutdown(tc)
}