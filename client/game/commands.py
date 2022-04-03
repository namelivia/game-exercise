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
    ClearInternalGameInformationEvent,
    GameCreatedEvent,
    PlayerJoinedEvent,
    PlayerPlacedSymbolEvent,
    PlaySoundEvent
)


# These put events on the queue requesting server interactions.
# ===== REQUESTS =====
class RequestPlaceASymbol(Command):
    def __init__(self, profile, queue, position):
        super().__init__(profile, queue, f'Request placing a symbol on position {position}')
        self.events = [
            PlaceASymbolRequestEvent(position)
        ]


class RequestGameCreation(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(profile, queue, f'Request creating a game called {new_game_name}')
        self.events = [
            NewGameRequestEvent(new_game_name)
        ]


class RequestJoiningAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f'Request joining game {game_id}')
        self.events = [
            JoinExistingGameEvent(game_id)
        ]


class RequestGameStatus(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f'Request refreshing the status of game {game_id}')
        self.events = [
            RefreshGameStatusEvent(game_id)
        ]
# ===================


# These are direct interactions with the server.
# ===== SERVER INTERACTIONS =====
class PlaceASymbol(Command):
    def __init__(self, profile, queue, game_id, position):
        super().__init__(profile, queue, f'Place a symbol on game {game_id} on position {position}')
        self.events = [
            PlaceASymbolNetworkRequestEvent(game_id, position)
        ]


class CreateAGame(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(profile, queue, f'Create a new game called {new_game_name}')
        self.events = [
            CreateAGameNetworkRequestEvent(new_game_name)
        ]


class JoinAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f'Join game {game_id}')
        self.events = [
            JoinAGameNetworkRequestEvent(game_id)
        ]


class RefreshGameStatus(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f'Refresh game status {game_id}')
        self.events = [
            RefreshGameStatusNetworkRequestEvent(game_id)
        ]

# ===================


# These are requests to change the screen.
# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Move back to lobby')
        self.events = [
            ClearInternalGameInformationEvent(),
            PlaySoundEvent('back'),
            ScreenTransitionEvent('lobby')
        ]


class ToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Move forward to lobby')
        self.events = [
            PlaySoundEvent('select'),
            ScreenTransitionEvent('lobby'),
        ]


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Move to new game screen')
        self.events = [
            PlaySoundEvent('select'),
            ScreenTransitionEvent('new_game_screen'),
        ]


class GoToJoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Move to join game screen')
        self.events = [
            PlaySoundEvent('select'),
            ScreenTransitionEvent('join_a_game'),
        ]

# ===================


# Things to do as a reaction to new events from the server
# ===== REACTIVE COMMANDS =====
class GameCreatedCommand(Command):
    def __init__(self, profile, queue, player_id):
        super().__init__(profile, queue, f'Player {player_id} created a game')
        self.events = [
            GameCreatedEvent(player_id),
        ]


class PlayerJoinedCommand(Command):
    def __init__(self, profile, queue, player_id):
        super().__init__(profile, queue, f'Player {player_id} joined the game')
        self.events = [
            PlayerJoinedEvent(player_id)
        ]


class PlayerPlacedSymbolCommand(Command):
    def __init__(self, profile, queue, player_id, position):
        super().__init__(profile, queue, f'Player {player_id} placed a symbol on position {position}')
        self.events = [
            PlayerPlacedSymbolEvent(player_id, position)
        ]


# These are other (generic?) events
# These could be non-game specific and be somewhere else
# ===== GENERIC =====
class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f'User typed key {key}')
        self.key = key

    def execute(self):
        self.queue.put(
            UserTypedEvent(self.key)
        )


class QuitGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, 'Exit from the game')

    def execute(self):
        self.queue.put(
            QuitGameEvent()
        )
