from common.messages import (
    PlaceASymbolMessage,
    CreateAGameMessage,
    JoinAGameMessage,
    GameMessage,
    ErrorMessage,
    GetGameStatus
)

from client.network.channel import Channel
from client.primitives.command import Command
from .events import (
    ScreenTransitionEvent,
    UserTypedEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    QuitGameEvent,
    InitiateGameEvent,
    PlaceASymbolRequestEvent,
    RefreshGameStatusEvent,
    UpdateGameEvent
)


# These put events on the queue requesting server interactions.
# ===== REQUESTS =====
class RequestPlaceASymbol(Command):
    def __init__(self, profile, queue, position):
        super().__init__(profile, 'Request placing a symbol')
        self.position = position
        self.queue = queue

    def execute(self):
        self.queue.put(
            PlaceASymbolRequestEvent(self.position)
        )


class RequestGameCreation(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(profile, 'Request the game creation')
        self.new_game_name = new_game_name
        self.queue = queue

    def execute(self):
        self.queue.put(
            NewGameRequestEvent(self.new_game_name)
        )


class RequestJoiningAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, 'Request joining an existing game')
        self.game_id = game_id
        self.queue = queue

    def execute(self):
        self.queue.put(
            JoinExistingGameEvent(self.game_id)
        )


class RequestGameStatus(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, 'Request refreshing the status of the game')
        self.game_id = game_id
        self.queue = queue

    def execute(self):
        self.queue.put(
            RefreshGameStatusEvent(self.game_id)
        )
# ===================


# These are direct interactions with the server.
# ===== SERVER INTERACTIONS =====
class PlaceASymbol(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Place a symbol on the board')
        self.queue = queue

    def execute(self, position):
        request_data = self._encode(position)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                self.queue.put(
                    UpdateGameEvent(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                )
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")

    def _encode(self, position):
        return PlaceASymbolMessage(self.profile.game_id, self.profile.id, position)


class CreateAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Create a new game')
        self.queue = queue

    def execute(self, new_game_name):
        request_data = self._encode(new_game_name)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                self.queue.put(
                    InitiateGameEvent(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                )
                self.profile.set_game(response.id)
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
                self.queue.put(
                    ScreenTransitionEvent('lobby')
                )
        else:
            print("Server error")
            self.queue.put(
                ScreenTransitionEvent('lobby')
            )

    def _encode(self, new_game_name):
        return CreateAGameMessage(new_game_name, self.profile.id)


class JoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Join a game')
        self.queue = queue

    def execute(self, game_id):
        request_data = self._encode(game_id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                self.queue.put(
                    InitiateGameEvent(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                )
                self.profile.set_game(response.id)
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")
            self.queue.put(
                ScreenTransitionEvent('lobby')
            )

    def _encode(self, game_id):
        return JoinAGameMessage(game_id, self.profile.id)


class RefreshGameStatus(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Refresh game status')
        self.queue = queue

    def execute(self, game_id):
        request_data = self._encode(game_id)

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameMessage):
                self.queue.put(
                    UpdateGameEvent(
                        response.id,
                        response.name,
                        response.turn,
                        response.board,
                        response.player_1_id,
                        response.player_2_id,
                    )
                )
            if isinstance(response, ErrorMessage):
                print(response.__dict__)
        else:
            print("Server error")

    def _encode(self, game_id):
        return GetGameStatus(game_id, self.profile.id)

# ===================


# These are requests to change the screen.
# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Back to lobby')
        self.queue = queue

    def execute(self):
        self.profile.set_game(None)
        self.queue.put(
            ScreenTransitionEvent('lobby')
        )


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Create a new game')
        self.queue = queue

    def execute(self):
        self.queue.put(
            ScreenTransitionEvent('new_game_screen')
        )


class GoToJoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Go to the join a game screen')
        self.queue = queue

    def execute(self):
        self.queue.put(
            ScreenTransitionEvent('join_a_game')
        )
# ===================


# These are other (generic?) events
# These could be non-game specific and be somewhere else
# ===== GENERIC =====
class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, 'User typed')
        self.queue = queue
        self.key = key

    def execute(self):
        self.queue.put(
            UserTypedEvent(self.key)
        )


class QuitGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Exit from the game')
        self.queue = queue

    def execute(self):
        self.queue.put(
            QuitGameEvent()
        )
