import socket
import sys
import threading
import RSA
import hashlib


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

        # create key pairs

        self.n_key, self.e_key, self.d_key = RSA.gen_keys()
        self.public_client_keys_msg = str(self.n_key) + " " + str(self.e_key)

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        try:
            self.s.sendall(self.username.encode())

            # exchange public keys
            msg = self.s.recv(1024).decode()
            self.server_n_key, self.server_e_key = map(int, msg.split())
            print("Received server public keys: {}, {}!".format(self.server_n_key, self.server_e_key))

            print("Sending public client keys to the server...")
            self.s.sendall(self.public_client_keys_msg.encode())

        except Exception as e:
            self.s.send("Not OK!".encode())
            print(e)
            print("Connection failed!")
            response = input()
            sys.exit()
        else:
            # final check
            self.s.send("OK!".encode())
            if self.s.recv(1024).decode() == "OK!":
                print("Safe connection established!")
            else:
                print("Connection failed!")
                response = input()
                sys.exit()

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        while True:
            packed_message = self.s.recv(1024).decode()
            try:
                space = packed_message.find(" ")
            except Exception:
                print("Received corrupted message!")
                continue
            hash, message = packed_message[:space], packed_message[space+1:]

            # decrypt message with the secrete key
            message = RSA.decode(message, self.n_key, self.d_key)

            if not hashlib.sha3_512(message.encode()).hexdigest() == hash:
                print("Received corrupted message: {}".format(message))

            print(message)

    def write_handler(self):
        while True:
            message = input()
            message_hash = hashlib.sha3_512(message.encode()).hexdigest()
            # encrypt message with the secrete key
            message = RSA.encode(message, self.server_n_key, self.server_e_key)
            packed_message = " ".join((message_hash, message))
            self.s.sendall(packed_message.encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "user")
    cl.init_connection()
