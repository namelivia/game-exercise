# from .screens import InGame
import socket
import pickle
from common.messages import (
    PlaceASymbolMessage,
    GameMessage,
    ErrorMessage,
    CreateAGameMessage,
    JoinAGameMessage,
)
from .constants import LOBBY, IN_GAME

ip, port = "localhost", 1234


# TODO: This will have to go somewhere else
def send_command(ip, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(pickle.dumps(message))
            return pickle.loads(sock.recv(1024))
    except ConnectionRefusedError:
        print("Could not connect to the server")


class PlaceASymbol:
    def __init__(self, profile):
        self.description = 'Place a symbol on the board'
        self.profile = profile

    def execute(self):
        # TODO: This should be somewhere else
        print('Where?')
        position = int(input('0, 1, 2, 3, 4 ,5, 6, 7, 8?'))
        request_data = self._encode(position)
        response = send_command(ip, port, request_data)
        # TODO: I should set this in the local game state, not passing it
        if isinstance(response, GameMessage):
            print(response.__dict__)
            return IN_GAME
        if isinstance(response, ErrorMessage):
            print(
                f"The server returned the following error: {response.message}"
            )

    def _encode(self, position):
        return PlaceASymbolMessage(self.profile.game_id, self.profile.id, position)


class CreateAGame:
    def __init__(self, profile):
        self.description = 'Create a new game'
        self.profile = profile

    def execute(self):
        game_name = input('Game name:')
        request_data = self._encode(game_name)
        response = send_command(ip, port, request_data)
        # TODO: I should set this in the local game state, not passing it
        if isinstance(response, GameMessage):
            self.profile.set_game(response.id)
            return IN_GAME
        if isinstance(response, ErrorMessage):
            print(
                f"The server returned the following error: {response.message}"
            )

    def _encode(self, game_name):
        return CreateAGameMessage(game_name, self.profile.id)


class JoinAGame:
    def __init__(self, profile):
        self.description = 'Join an existing game'
        self.profile = profile

    def execute(self):
        game_id = input('Game id:')
        request_data = self._encode(game_id)
        response = send_command(ip, port, request_data)
        # TODO: I should set this in the local game state, not passing it
        if isinstance(response, GameMessage):
            self.profile.set_game(response.id)
            return IN_GAME
        if isinstance(response, ErrorMessage):
            print(
                f"The server returned the following error: {response.message}"
            )
            return LOBBY

    def _encode(self, game_id):
        return JoinAGameMessage(game_id, self.profile.id)


class LeaveTheGame:
    def __init__(self, profile):
        self.description = 'Leave the existing game'
        self.profile = profile

    def execute(self):
        self.profile.set_game(None)
        return LOBBY
