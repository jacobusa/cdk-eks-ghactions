package main

import (
	"fmt"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)


func regionFromEnv(w http.ResponseWriter, req *http.Request) {
	awsRegion := os.Getenv("AWS_REGION")
	fmt.Fprintf(w, awsRegion)
}

func main() {
	godotenv.Load("../.env")
	http.HandleFunc("/region", regionFromEnv)

	log.Println("Server started on port: 9090")
	log.Fatal(http.ListenAndServe(":9090", nil))
}