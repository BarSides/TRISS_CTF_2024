# Title

Bad Malware

## Overview

We have samples of this first stage malware (a dropper). The malware downloads an encrypted payload that seems to be generated. Analyze the malware, modify it and then use it to connect to the server to download and decrypt the latest payload, which contains the flag.

`droppers.zip` contains the samples and their sample payloads (these do not contain the real flag).

You can point the dropper at a particular URL with this env var:

`CTF_SERVER_URL=http://example.com:8890/flag ./dropper ...`