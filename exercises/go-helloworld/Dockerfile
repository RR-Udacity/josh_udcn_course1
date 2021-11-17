FROM golang:alpine
# FROM jdhaines/go-helloworld:v1.0.0
WORKDIR /go/src/app
ADD . .
EXPOSE 6111
# RUN go mod download
RUN go build -o helloworld
CMD ["./helloworld"]