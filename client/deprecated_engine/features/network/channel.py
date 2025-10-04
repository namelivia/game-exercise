import logging
import pickle
import socket
from typing import Any, Optional

IP = "localhost"
PORT = 1234
logger = logging.getLogger(__name__)


class Channel:
    @staticmethod
    def send_command(message: Any) -> Optional[Any]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((IP, PORT))
                sock.sendall(pickle.dumps(message))
                response = pickle.loads(sock.recv(1024))
                return response
        except ConnectionRefusedError:
            logger.error("Could not connect to the server")
            return None
        except EOFError:
            logger.error("EOF pickle error, the message could not be sent")
            return None
