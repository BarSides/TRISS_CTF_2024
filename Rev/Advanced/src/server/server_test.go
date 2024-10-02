package main

import (
	"encoding/base64"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestFlagHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/flag", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(flagHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	encodedFlag := rr.Body.String()
	if _, err := base64.StdEncoding.DecodeString(encodedFlag); err != nil {
		t.Errorf("handler returned invalid base64: %v", err)
	}
}

func TestEncodeFlag(t *testing.T) {
	encoded := encodeFlag()
	if encoded == "" {
		t.Error("encodeFlag returned empty string")
	}

	if _, err := base64.StdEncoding.DecodeString(encoded); err != nil {
		t.Errorf("encodeFlag returned invalid base64: %v", err)
	}
}

func TestObfuscate(t *testing.T) {
	input := []byte("Hello, World!")
	obfuscated := obfuscate(input)
	deobfuscated := obfuscate(obfuscated)

	if string(deobfuscated) != string(input) {
		t.Errorf("obfuscate is not reversible: got %s, want %s", deobfuscated, input)
	}
}

func TestXorEncrypt(t *testing.T) {
	input := []byte("Test input")
	key := "TestKey"
	encrypted := xorEncrypt(input, key)
	decrypted := xorEncrypt(encrypted, key)

	if string(decrypted) != string(input) {
		t.Errorf("xorEncrypt is not reversible: got %s, want %s", decrypted, input)
	}
}

func TestEncryptAES(t *testing.T) {
	input := []byte("Test AES encryption")
	encrypted, err := encryptAES(input)
	if err != nil {
		t.Fatalf("encryptAES failed: %v", err)
	}

	if len(encrypted) <= len(input) {
		t.Errorf("encrypted data is not longer than input: got %d, want > %d", len(encrypted), len(input))
	}

	if strings.Contains(string(encrypted), string(input)) {
		t.Errorf("encrypted data contains plaintext")
	}
}