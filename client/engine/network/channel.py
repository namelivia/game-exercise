import socket
import pickle

IP = "localhost"
PORT = 1234


class Channel:
    @staticmethod
    def send_command(message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((IP, PORT))
                sock.sendall(pickle.dumps(message))
                response = pickle.loads(sock.recv(1024))
                return response
        except ConnectionRefusedError:
            print("Could not connect to the server")
            return None
