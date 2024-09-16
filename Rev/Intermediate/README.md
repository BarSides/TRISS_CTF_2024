# Reverse Engineering Intermediate Challenge: Encrypted Dropper

## Challenge Description

In this challenge, you're presented with a mysterious dropper executable that connects to a local server to retrieve an encrypted flag. Your task is to reverse engineer the dropper, understand its decryption process, and ultimately retrieve the flag.

## Setup Instructions

1. Start the server by running the `server` binary in the background:
   ```
   ./server &
   ```
2. The server will start running on `http://localhost:8080`.

## Challenge Instructions

1. You are provided with a `dropper` binary.
2. Run the dropper:
   ```
   ./dropper
   ```
3. The dropper will attempt to connect to the server, retrieve an encrypted flag, and then decrypt it.
4. Your goal is to understand the encryption and decryption processes used in the dropper.
5. Analyze the binary to identify the encryption keys and algorithms used in the process.
6. Once you understand the process, you can either modify the dropper or create your own script to successfully decrypt the flag.

## Hints

1. The dropper uses multiple layers of encryption and obfuscation.
2. Look for any hardcoded strings or constants in the binary that might be used as encryption keys.
3. The decryption process may involve base64 decoding, AES decryption, XOR operations, and deobfuscation.
4. Some functions in the code might be there to make the challenge more interesting. Focus on the main decryption flow.

Good luck, and happy reversing!
