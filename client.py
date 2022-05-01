import socket
import sys
import threading
import fake_rsa  # change on the real lib, when finished!


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

        # create key pairs

        self.n_key, self.e_key, self.d_key = fake_rsa.generate_keys()
        self.public_client_keys_msg = str(self.n_key) + " " + str(self.e_key)

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        try:
            self.s.send(self.username.encode())

            # exchange public keys
            msg = self.s.recv(1024).decode()
            self.server_n_key, self.server_e_key = msg.split()
            print("Received server public keys: {}, {}!".format(self.server_n_key, self.server_e_key))

            print("Sending public client keys to the server...")
            self.s.send(self.public_client_keys_msg.encode())

            # receive the encrypted secret key
            self.server_d_key = fake_rsa.decode(self.s.recv(1024).decode(), self.d_key)
            self.server_d_key = "d_key"
            print("Received server secret key!")

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

        print("Server secret key: {}".format(self.server_d_key))

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key
            message = fake_rsa.decode(message, self.server_d_key)

            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key
            message = fake_rsa.encode(message, self.server_n_key, self.server_e_key)

            self.s.send(message.encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "user")
    cl.init_connection()
