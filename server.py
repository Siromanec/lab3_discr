import socket
import threading
import fake_rsa


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # generate keys ...

        print("Generating server keys...")
        self.n_key, self.e_key, self.d_key = fake_rsa.generate_keys()
        self.public_server_keys_msg = str(self.n_key) + " " + str(self.e_key)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        while True:
            try:
                print("Waiting for a new connections...")
                c, addr = self.s.accept()
                username = c.recv(1024).decode()
                print(f"{username} tries to connect")
                self.broadcast(f'new person has joined: {username}')
                self.username_lookup[c] = username
                self.clients.append(c)

                # send public key to the client
                print("Sending keys to {}".format(self.username_lookup[c]))
                c.send(self.public_server_keys_msg.encode())
                print("Public keys to {} sent!".format(self.username_lookup[c]))
                # ...
                while True:
                    public_client_keys_msg = c.recv(1024).decode()
                    if public_client_keys_msg:
                        client_n, client_d = public_client_keys_msg.split()
                        break
                print("Client {} public keys received!".format(self.username_lookup[c]))

                # encrypt the secret with the clients public key

                encrypted_d_key = fake_rsa.encode(self.d_key, client_n, client_d)

                # send the encrypted secret to a client

                print("Sending encrypted secret key to client {}!".format(self.username_lookup[c]))
                c.send(encrypted_d_key.encode())

                # final check
                if c.recv(1024).decode() != "OK!":
                    raise ConnectionError("Problems on the client side, safe connection wasn't established\n")
                c.send("OK!".encode())

                threading.Thread(target=self.handle_client,args=(c,addr,)).start()
            except Exception as e:
                print(e)
                try:
                    c.send("Not OK!".encode())
                except Exception:
                    pass
            else:
                print("Safe connection established!\n")

    def broadcast(self, msg: str):
        for client in self.clients: 

            # encrypt the message
            msg = fake_rsa.encode(msg, self.n_key, self.e_key)
            # ...

            client.send(msg.encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)


if __name__ == "__main__":
    s = Server(9001)
    s.start()
