```
$ dd if=./forensics_beginner.veracrypt of=./header.veracrypt bs=512 count=1 
$ hashcat -a3 -w1 -m13721 ./header.veracrypt /usr/share/wordlists/fasttrack.txt
$ sudo veracrypt ./forensics_beginner.veracrypt /media/veracrypt26 --password guessme
$ ls /media/veracrypt26
flag.txt
```

Source: https://codeonby.com/2022/01/19/brute-force-veracrypt-encryption/

The password is "guessme".

Flag: TRISS{v3ry_v3ry_v3r4crypt3d}