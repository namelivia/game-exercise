from client.engine.primitives.command import Command
from .events import (
    QuitGameEvent,
    UserTypedEvent,
    UpdateGameEvent,
    InitiateGameEvent,
    SetInternalGameInformationEvent,
    SetPlayerNameEvent,
    GameCreatedInGameEvent,
    PlayerJoinedInGameEvent,
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    PlayerPlacedSymbolInGameEvent,
    ChatMessageInGameEvent,
    NewGameRequestEvent,
    JoinExistingGameEvent,
    CreateAGameNetworkRequestEvent,
    JoinAGameNetworkRequestEvent,
    PingNetworkRequestEvent,
    GetGameListNetworkRequestEvent,
    UpdateGameListEvent,
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    ErrorGettingGameListEvent,
    ErrorCreatingGameEvent,
    ErrorJoiningGameEvent,
)

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


class UserTyped(Command):
    def __init__(self, profile, queue, key):
        super().__init__(profile, queue, f"User typed key {key}")
        self.key = key

    def execute(self):
        self.queue.put(UserTypedEvent(self.key))


class TurnSoundOn(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Turning sound ON")
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Turning sound OFF")
        self.events = [
            TurnSoundOffEvent(),
        ]


# ======= GAME STATE SYNC =======
class InitiateGame(Command):
    def __init__(self, profile, queue, game_data):
        super().__init__(profile, queue, f"Locally initializing game {game_data.id}")
        self.events = [
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


class UpdateGame(Command):
    def __init__(self, profile, queue, events):
        super().__init__(profile, queue, "Locally updating game")
        self.events = [UpdateGameEvent(events)]


class UpdateGameList(Command):
    def __init__(self, profile, queue, games):
        super().__init__(profile, queue, "Updating game list")
        self.events = [UpdateGameListEvent(games)]


# This says server events but these are GAME events (put on the game data by the server)
class ProcessServerEvents(Command):
    def __init__(self, profile, queue, events):
        super().__init__(
            profile, queue, f"Processing {len(events)} unprocessed server events"
        )
        self.events = events


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


# This one seems specific
class PlayerPlacedSymbolInGameCommand(Command):
    def __init__(self, profile, queue, player_id, position):
        super().__init__(
            profile, queue, f"Player {player_id} placed a symbol on position {position}"
        )
        self.events = [
            PlayerPlacedSymbolInGameEvent(
                player_id, position
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


# This one seems specific
class ChatMessageInGameCommand(Command):
    def __init__(self, profile, queue, player_id, message):
        super().__init__(profile, queue, f"Player {player_id} says: {message}")
        self.events = [
            ChatMessageInGameEvent(
                player_id, message
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


# ==== This one is to request the game status (polling)
class RequestGameStatus(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(
            profile, queue, f"Request refreshing the status of game {game_id}"
        )
        self.events = [RefreshGameStatusEvent(game_id)]


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
class RefreshGameStatus(Command):
    def __init__(self, profile, queue, game_id):
        super().__init__(profile, queue, f"Refresh game status {game_id}")
        self.events = [RefreshGameStatusNetworkRequestEvent(game_id)]


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


class GetGameList(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Get Game List")
        self.events = [GetGameListNetworkRequestEvent()]


# ==== Errors
class ErrorGettingGameList(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Getting Game List")
        self.events = [ErrorGettingGameListEvent()]


class ErrorCreatingGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Creating game")
        self.events = [ErrorCreatingGameEvent()]


class ErrorJoiningGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Joining game")
        self.events = [ErrorJoiningGameEvent()]