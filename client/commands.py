# from .screens import InGame
from common.messages import (
    PlaceASymbolMessage,
    CreateAGameMessage,
    JoinAGameMessage,
)
from .constants import LOBBY, IN_GAME
from .channel import Channel
from abc import ABC


class Command(ABC):

    def __init__(self, profile, description):
        self.description = description
        self.profile = profile

    def execute():
        pass


class PlaceASymbol:
    def __init__(self, profile):
        super().__init__(profile, 'Place a symbol on the board')

    def execute(self):
        # TODO: This should be a different screen
        print('Where?')
        position = int(input('0, 1, 2, 3, 4 ,5, 6, 7, 8?'))
        request_data = self._encode(position)

        response = Channel.send_command(request_data)
        if response is not None:
            return IN_GAME

    def _encode(self, position):
        return PlaceASymbolMessage(self.profile.game_id, self.profile.id, position)


class CreateAGame:
    def __init__(self, profile):
        super().__init__(profile, 'Create a new game')

    def execute(self):
        game_name = input('Game name:')
        request_data = self._encode(game_name)

        response = Channel.send_command(request_data)
        if response is not None:
            return IN_GAME

    def _encode(self, game_name):
        return CreateAGameMessage(game_name, self.profile.id)


class JoinAGame:
    def __init__(self, profile):
        super().__init__(profile, 'Join an existing game')

    def execute(self):
        game_id = input('Game id:')
        request_data = self._encode(game_id)
        response = Channel.send_command(request_data)
        response = Channel.send_command(request_data)
        if response is not None:
            return IN_GAME
        return LOBBY

    def _encode(self, game_id):
        return JoinAGameMessage(game_id, self.profile.id)


class LeaveTheGame:
    def __init__(self, profile):
        super().__init__(profile, 'LeaveTheGame')

    def execute(self):
        self.profile.set_game(None)
        return LOBBY
