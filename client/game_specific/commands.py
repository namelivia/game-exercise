# from .screens import InGame
from common.messages import (
    PlaceASymbolMessage,
    CreateAGameMessage,
    JoinAGameMessage,
)
from .constants import LOBBY, IN_GAME
from client.network.channel import Channel
from .events import ScreenTransitionEvent, UserTypedEvent
from abc import ABC


class Command(ABC):

    def __init__(self, profile, description):
        self.description = description
        self.profile = profile

    def execute():
        pass


class PlaceASymbol(Command):
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


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Create a new game')
        self.queue = queue

    def execute(self):
        self.queue.put(
            ScreenTransitionEvent('new_game_screen')
        )


class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Back to lobby')
        self.queue = queue

    def execute(self):
        self.queue.put(
            ScreenTransitionEvent('lobby')
        )


class CreateAGame(Command):
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


class JoinAGame(Command):
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


class LeaveTheGame(Command):
    def __init__(self, profile):
        super().__init__(profile, 'Leave the game')

    def execute(self):
        self.profile.set_game(None)
        return LOBBY


class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, 'User typed')
        self.queue = queue
        self.key = key

    def execute(self):
        self.queue.put(
            UserTypedEvent(self.key)
        )
