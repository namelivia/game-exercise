from client.primitives.command import Command
from .events import (
    ScreenTransitionEvent,
    UserTypedEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    QuitGameEvent,
    PlaceASymbolRequestEvent,
    PlaceASymbolNetworkRequestEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    RefreshGameStatusNetworkRequestEvent,
    RefreshGameStatusEvent,
    GameCreatedEvent,
    PlayerJoinedEvent,
    PlayerPlacedSymbolEvent,
    PlaySoundEvent
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

    def execute(self, game_id, position):
        self.queue.put(
            PlaceASymbolNetworkRequestEvent(game_id, position)
        )


class CreateAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Create a new game')
        self.queue = queue

    def execute(self, new_game_name):
        self.queue.put(
            CreateAGameNetworkRequestEvent(new_game_name)
        )


class JoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Join a game')
        self.queue = queue

    def execute(self, game_id):
        self.queue.put(
            JoinAGameNetworkRequestEvent(game_id)
        )


class RefreshGameStatus(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Refresh game status')
        self.queue = queue

    def execute(self, game_id):
        self.queue.put(
            RefreshGameStatusNetworkRequestEvent(game_id)
        )

# ===================


# These are requests to change the screen.
# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Move back to lobby')
        self.queue = queue

    def execute(self):
        self.profile.set_game(None)
        self.profile.set_game_event_pointer(None)
        self.queue.put(
            PlaySoundEvent('back')
        )
        self.queue.put(
            ScreenTransitionEvent('lobby')
        )


class ToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Move forward to lobby')
        self.queue = queue

    def execute(self):
        self.queue.put(
            PlaySoundEvent('select')
        )
        self.queue.put(
            ScreenTransitionEvent('lobby')
        )


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Create a new game')
        self.queue = queue

    def execute(self):
        self.queue.put(
            PlaySoundEvent('select')
        )
        self.queue.put(
            ScreenTransitionEvent('new_game_screen')
        )


class GoToJoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Go to the join a game screen')
        self.queue = queue

    def execute(self):
        self.queue.put(
            PlaySoundEvent('select')
        )
        self.queue.put(
            ScreenTransitionEvent('join_a_game')
        )
# ===================


# Things to do as a reaction to new events from the server
# ===== REACTIVE COMMANDS =====
class GameCreatedCommand(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'A player created a game')
        self.queue = queue

    def execute(self, player_id):
        self.queue.put(
            GameCreatedEvent(player_id)
        )


class PlayerJoinedCommand(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'User typed')
        self.queue = queue

    def execute(self, player_id):
        self.queue.put(
            PlayerJoinedEvent(player_id)
        )


class PlayerPlacedSymbolCommand(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, 'Player placed a symbol')
        self.queue = queue

    def execute(self, player_id, position):
        self.queue.put(
            PlayerPlacedSymbolEvent(player_id, position)
        )


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
