package stats

import (
	"bytes"
	"encoding/json"
	"net"
)

type ResponseMessage struct {
	Code string `json:"code"`
	Message string `json:"message"`
}

// Main listener for incoming client data, listening on port 4050 on TCP.
func Listener()  {
	listener, err := net.Listen("tcp", "0.0.0.0:4050")
	defer listener.Close()
	if err != nil {
		panic(err)
	}
	for {
		conn, err := listener.Accept()
		if err != nil {
			// handle error
		}
		go Handler(conn)
	}
}

// Handles individual connections, parsing JSON data from client and writing a message.
func Handler(c net.Conn) {
	defer c.Close()
	var b bytes.Buffer

	// Read data in from client.
	buffer := make([]byte, 1024)
	len, err := c.Read(buffer)
	if err != nil {
		WriteMessage("error", "Unable to read client message", c)
	}
	b.Write(buffer)
	b.Truncate(len)

	WriteMessage("success", "Read and parsed client message", c)
}

// Write ResponseMessage out to connection.
func WriteMessage(code string, message string, c net.Conn) {
	result := ResponseMessage{
		Code: code,
		Message: message,
	}
	resultJson, err := json.Marshal(result)
	if err != nil {
		panic(err)
	}

	_, err = c.Write(resultJson)
	if err != nil {
		panic(err)
	}
}