package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
	"os"
)

var (
	flag     = os.Getenv("CTF_FLAG")
	xorKey   = os.Getenv("CTF_XOR_KEY")
	aesKey   = os.Getenv("CTF_AES_KEY")
	httpPort = os.Getenv("CTF_SERVER_PORT")
)

func main() {
	http.HandleFunc("/flag", flagHandler)
	fmt.Printf("Server running on http://localhost:%s\n", httpPort)
	http.ListenAndServe(":"+httpPort, nil)
}

func flagHandler(w http.ResponseWriter, r *http.Request) {
	encodedFlag := encodeFlag()
	w.Write([]byte(encodedFlag))
}

func encodeFlag() string {
	// Obfuscate
	obfuscated := obfuscate([]byte(flag))

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