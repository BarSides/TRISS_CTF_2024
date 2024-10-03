package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

var (
	httpPort = os.Getenv("CTF_PORT")
	xorKey   string
	aesKey   string
)

func generateKeys() (string, string) {
	var dateStr string
	if envDate := os.Getenv("CTF_DATE"); envDate != "" {
		dateStr = envDate
	} else {
		now := time.Now().UTC()
		dateStr = now.Format("20060102")
	}
	xorKey := "CTF" + dateStr
	aesKey := "CTF" + dateStr + "_AES!" // Ensure AES key is 16, 24, or 32 bytes long
	return xorKey, aesKey
}

func main() {
	outputFile := flag.String("output", "", "Output file for the payload")
	flag.Parse()

	xorKey, aesKey = generateKeys()
	
	encodedPayload := encodePayload()

	if *outputFile != "" {
		err := os.WriteFile(*outputFile, []byte(encodedPayload), 0644)
		if err != nil {
			log.Fatalf("Error writing payload to file: %v", err)
		}
		fmt.Printf("Payload written to %s\n", *outputFile)
	} else {
		http.HandleFunc("/flag", flagHandler)
	
	fmt.Printf("Server running on http://0.0.0.0:%s\n", httpPort)
		fmt.Printf("Using XOR Key: %s, AES Key: %s\n", xorKey, aesKey)
		
		err := http.ListenAndServe("0.0.0.0:"+httpPort, nil)
		if err != nil {
			log.Fatalf("Error starting server: %v", err)
		}
	}
}

func flagHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Serving flag to", r.RemoteAddr)
	encodedPayload := encodePayload()
	w.Write([]byte(encodedPayload))
}

func encodePayload() string {
	payload := os.Getenv("CTF_FLAG")
	if payload == "" {
		payload = "BarSides{DEFAULT_FLAG}"
	}

	// Obfuscate
	obfuscated := obfuscate([]byte(payload))

	// XOR encrypt
	xorEncrypted := xorEncrypt(obfuscated, xorKey)

	// AES encrypt
	aesEncrypted, err := encryptAES(xorEncrypted)
	if err != nil {
		fmt.Println("Error encrypting with AES:", err)
		return ""
	}

	// Base64 encode
	encoded := base64.StdEncoding.EncodeToString(aesEncrypted)

	return encoded
}

func obfuscate(input []byte) []byte {
	// Simple obfuscation: reverse the string
	runes := []rune(string(input))
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return []byte(string(runes))
}

func xorEncrypt(input []byte, key string) []byte {
	output := make([]byte, len(input))
	for i := 0; i < len(input); i++ {
		output[i] = input[i] ^ key[i%len(key)]
	}
	return output
}

func encryptAES(plaintext []byte) ([]byte, error) {
	block, err := aes.NewCipher([]byte(aesKey))
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		return nil, err
	}

	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)

	return ciphertext, nil
}