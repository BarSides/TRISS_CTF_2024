# Name

Crypt You Very Much

## Overview

Your task is to crack this Veracrypt volume.

The veracrypt file was encrypted with a password from the file /usr/share/wordlist/fasttrack.txt easily found on kali linux.

```
$ md5sum /usr/share/wordlists/fasttrack.txt 
b07e127fe3b4386288ec86593eb0a011  /usr/share/wordlists/fasttrack.txt
```

Hint: `truecrack` didn't work for me. 

The veracrypt volume was encrypted with AES, hashing algorithm SHA-512.