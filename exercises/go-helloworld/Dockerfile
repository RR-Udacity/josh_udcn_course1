# FROM golang:alpine
FROM jdhaines/go-helloworld:v1.0.0
WORKDIR /go/src/app
COPY . .
RUN go mod download
RUN go build -o helloworld
