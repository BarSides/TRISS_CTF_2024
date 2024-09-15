package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

const (
	serverURL = "http://localhost:8080/flag"
	xorKey    = "TRISS_CTF_2024"
	aesKey    = "TRISS_CTF_2024_1" // AES key must be 16, 24, or 32 bytes long
)

func main() {
	// Download the encoded flag from the server
	encodedFlag, err := downloadFlag()
	if err != nil {
		fmt.Println("Error downloading flag:", err)
		os.Exit(1)
	}

	// Decode the flag from base64
	decodedFlag, err := base64.StdEncoding.DecodeString(encodedFlag)
	if err != nil {
		fmt.Println("Error decoding base64:", err)
		os.Exit(1)
	}

	// Decrypt the flag using AES
	decryptedFlag, err := decryptAES(decodedFlag)
	if err != nil {
		fmt.Println("Error decrypting AES:", err)
		os.Exit(1)
	}

	// XOR decrypt the flag
	xorDecrypted := xorDecrypt(decryptedFlag, xorKey)

	// Deobfuscate the flag
	flag := deobfuscate(xorDecrypted)

	fmt.Println("Flag:", flag)
}

func downloadFlag() (string, error) {
	resp, err := http.Get(serverURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}

func decryptAES(ciphertext []byte) ([]byte, error) {
	block, err := aes.NewCipher([]byte(aesKey))
	if err != nil {
		return nil, err
	}

	if len(ciphertext) < aes.BlockSize {
		return nil, fmt.Errorf("ciphertext too short")
	}

	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(ciphertext, ciphertext)

	return ciphertext, nil
}

func xorDecrypt(input []byte, key string) []byte {
	output := make([]byte, len(input))
	for i := 0; i < len(input); i++ {
		output[i] = input[i] ^ key[i%len(key)]
	}
	return output
}

func deobfuscate(input []byte) string {
	// Simple deobfuscation: reverse the string
	runes := []rune(string(input))
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// Extra function to make the code more interesting for CTF participants
func obfuscatedFunction() string {
	var s string
	for _, v := range []int{84, 82, 73, 83, 83, 95, 67, 84, 70} {
		s += string(rune(v))
	}
	return s
}
