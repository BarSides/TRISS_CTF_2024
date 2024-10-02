# Title

Bad Malware

## Overview

We have samples of this first stage malware (a dropper). The malware downloads an encrypted payload that seems to be generated. Analyze the malware and decrypt the latest payload, which contains the flag.

`droppers.zip` contains the samples and their payloads.

You can point the dropper at a particular URL with this env var:

`CTF_SERVER_URL=http://example.com:8080/flag ./dropper ...`