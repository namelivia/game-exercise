from client.engine.primitives.command import Command
from .events import (
    QuitGameEvent,
    InitiateGameEvent,
    SetInternalGameInformationEvent,
    SetPlayerNameEvent,
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    PingNetworkRequestEvent,
    ErrorCreatingGameEvent,
    ErrorJoiningGameEvent,
)
from client.engine.features.sound.events import PlaySoundEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# ======= GENERIC =======
class QuitGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Exit from the game")

    def execute(self):
        self.queue.put(QuitGameEvent())


# ======= GAME STATE SYNC =======
class InitiateGame(Command):
    def __init__(self, profile, queue, game_data):
        super().__init__(profile, queue, f"Locally initializing game {game_data.id}")
        self.events = [
            PlaySoundEvent("start_game"),
            InitiateGameEvent(
                game_data
            ),  # Event to be picked up by the game event handler
            SetInternalGameInformationEvent(game_data.id),
        ]


class SetPlayerName(Command):
    def __init__(self, profile, queue, name):
        super().__init__(profile, queue, "Setting player name")
        self.events = [
            SetPlayerNameEvent(name),
        ]


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameCommand(Command):
    def __init__(self, profile, queue, player_id):
        super().__init__(profile, queue, f"Player {player_id} created a game")
        # Then who starts GameCreated??
        # IT IS AN EVENT ON THE GAME QUEUE, AND BECAUSE OF THAT IT IS PUT ON THE EVENTS ARRAY BY THE SERVER
        # GameCreated => GameCreatedEventHandler => GameCreatedCommand => GameCreatedEvent
        self.events = [
            GameCreatedInGameEvent(
                player_id
            ),  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class PlayerJoinedInGameCommand(Command):
    def __init__(self, profile, queue, player_id):
        super().__init__(profile, queue, f"Player {player_id} joined the game")
        self.events = [
            PlayerJoinedInGameEvent(
                player_id
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class PlayerWinsInGameCommand(Command):
    def __init__(self, profile, queue, player_id):
        super().__init__(profile, queue, f"Player {player_id} wins the game")
        self.events = [
            PlayerWinsInGameEvent(
                player_id
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class RequestGameCreation(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(
            profile, queue, f"Request creating a game called {new_game_name}"
        )
        self.events = [NewGameRequestEvent(new_game_name)]


class RequestJoiningAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f"Request joining game {game_id}")
        self.events = [JoinExistingGameEvent(game_id)]


# ==== These are network requests
class CreateAGame(Command):
    def __init__(self, profile, queue, new_game_name):
        super().__init__(profile, queue, f"Create a new game called {new_game_name}")
        self.events = [CreateAGameNetworkRequestEvent(new_game_name)]


class JoinAGame(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f"Join game {game_id}")
        self.events = [JoinAGameNetworkRequestEvent(game_id)]


class PingTheServer(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Ping the server")
        self.events = [PingNetworkRequestEvent()]


# ==== Errors
class ErrorCreatingGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Creating game")
        self.events = [ErrorCreatingGameEvent()]


class ErrorJoiningGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Joining game")
        self.events = [ErrorJoiningGameEvent()]
