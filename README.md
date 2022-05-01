## Usage example
![](usage_example.png)

## Usage instruction
- Open server.py
- Open client.py multiple times
- Write message in the one window to receive it on others

## How it works
- Client establishes connection with a server by exchanging public keys(RSA).
- Each time client sends a message, it encodes it using server public RSA keys. Server decodes it using own secret key. Then, server encodes message again, for each client individually, using public keys of that client. Finally, client receives and decodes message.
- Additionally, there is a verification of message integrity using hash keys.