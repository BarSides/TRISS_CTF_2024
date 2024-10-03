package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"io"
	"testing"
)

func TestDecryptAES(t *testing.T) {
	plaintext := []byte("Test AES decryption")
	block, _ := aes.NewCipher([]byte(aesKey))
	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		t.Fatal(err)
	}
	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)

	decrypted, err := decryptAES(ciphertext)
	if err != nil {
		t.Fatalf("decryptAES failed: %v", err)
	}

	if !bytes.Equal(decrypted, plaintext) {
		t.Errorf("decryptAES failed: got %s, want %s", decrypted, plaintext)
	}
}

func TestXorDecrypt(t *testing.T) {
	input := []byte("Test XOR decryption")
	key := "TestKey"
	
	encrypted := xorEncrypt(input, key) // We need to implement this function
	decrypted := xorDecrypt(encrypted, key)

	if !bytes.Equal(decrypted, input) {
		t.Errorf("xorDecrypt failed: got %s, want %s", decrypted, input)
	}
}

func TestDeobfuscate(t *testing.T) {
	input := "!dlroW ,olleH"
	expected := "Hello, World!"
	result := deobfuscate([]byte(input))

	if result != expected {
		t.Errorf("deobfuscate failed: got %s, want %s", result, expected)
	}
}

func TestObfuscatedFunction(t *testing.T) {
	expected := "TRISS_CTF"
	result := obfuscatedFunction()

	if result != expected {
		t.Errorf("obfuscatedFunction failed: got %s, want %s", result, expected)
	}
}

// Helper function for XOR encryption (same as XOR decryption)
func xorEncrypt(input []byte, key string) []byte {
	output := make([]byte, len(input))
	for i := 0; i < len(input); i++ {
		output[i] = input[i] ^ key[i%len(key)]
	}
	return output
}