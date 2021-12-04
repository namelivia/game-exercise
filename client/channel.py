import socket
import pickle
from common.messages import (
    GameMessage,
    ErrorMessage,
)

IP = "localhost"
PORT = 1234


class Channel():

    @staticmethod
    def send_command(message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((IP, PORT))
                sock.sendall(pickle.dumps(message))
                response = pickle.loads(sock.recv(1024))
        except ConnectionRefusedError:
            print("Could not connect to the server")
            return None
        if isinstance(response, GameMessage):
            return response
        if isinstance(response, ErrorMessage):
            print(
                f"The server returned the following error: {response.message}"
            )
        return None
