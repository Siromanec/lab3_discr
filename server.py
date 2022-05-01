import socket
import threading
import RSA


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.users_keys = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # generate keys ...
        try:
            print("Generating server keys...")
            self.n_key, self.e_key, self.d_key = RSA.gen_keys()
            self.public_server_keys_msg = str(self.n_key) + " " + str(self.e_key)
        except Exception as e:
            print(e)

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
                public_client_keys_msg = c.recv(1024).decode()
                client_n, client_e = map(int, public_client_keys_msg.split())
                print("Client {} public keys received!".format(self.username_lookup[c]))
                self.users_keys[c] = (client_n, client_e)

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
        if not isinstance(msg, str):
            msg = RSA.decode(msg.decode(), self.n_key, self.d_key)
        for client in self.clients: 

            # encrypt the message
            encoded_msg = RSA.encode(msg, self.users_keys[client][0], self.users_keys[client][1])
            client.send(encoded_msg.encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024).decode()
            msg = RSA.decode(msg, self.n_key, self.d_key)
            for client in self.clients:
                encoded_msg = RSA.encode(msg, self.users_keys[client][0], self.users_keys[client][1])
                if client != c:
                    client.send(encoded_msg.encode())


if __name__ == "__main__":
    s = Server(9001)
    s.start()
