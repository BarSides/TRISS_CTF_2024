package main

import (
    "crypto/aes"
    "crypto/cipher"
    "encoding/base64"
    "flag"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
)

var (
    serverURL = os.Getenv("CTF_SERVER_URL")
)

// Template variables filled during compilation
var (
    xorKey = "CTF20230515"
    aesKey = "CTF20230515_AES!"
)

func main() {
    outputFile := flag.String("output", "", "Output file for the raw downloaded payload")
    dumpBinary := flag.Bool("dump", false, "Dump the binary payload to a file")
    flag.Parse()

    if serverURL == "" {
        serverURL = "http://localhost:8080/flag"
    }

    // Download the encoded flag from the server
    encodedFlag, err := downloadFlag(serverURL)
    if err != nil {
        fmt.Println("Error downloading flag:", err)
        os.Exit(1)
    }

    // Optionally write the raw payload to a file
    if *outputFile != "" {
        err = ioutil.WriteFile(*outputFile, []byte(encodedFlag), 0644)
        if err != nil {
            fmt.Println("Error writing to file:", err)
            os.Exit(1)
        }
        fmt.Println("Raw payload written to", *outputFile)
        if !*dumpBinary {
            return
        }
    }

    // Decode the flag from base64
    decodedFlag, err := base64.StdEncoding.DecodeString(encodedFlag)
    if err != nil {
        fmt.Println("Error decoding base64:", err)
        os.Exit(1)
    }

    // Optionally dump the binary payload
    if *dumpBinary {
        binaryFile := "binary_payload.bin"
        if *outputFile != "" {
            binaryFile = *outputFile + ".bin"
        }
        err = ioutil.WriteFile(binaryFile, decodedFlag, 0644)
        if err != nil {
            fmt.Println("Error writing binary payload to file:", err)
            os.Exit(1)
        }
        fmt.Println("Binary payload written to", binaryFile)
        return
    }

    // Decrypt the flag using AES
    decryptedFlag, err := decryptAES(decodedFlag, aesKey)
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

func downloadFlag(serverURL string) (string, error) {
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

func decryptAES(ciphertext []byte, aesKey string) ([]byte, error) {
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