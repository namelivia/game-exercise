from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

if TYPE_CHECKING:
    from common.game_data import GameData
    from uuid import UUID

from client.engine.features.sound.events import PlaySoundEvent

from .events import (
    GameCreatedInGameEvent,
    InitiateGameEvent,
    PingNetworkRequestEvent,
    PlayerJoinedInGameEvent,
    PlayerWinsInGameEvent,
    QuitGameEvent,
    SetInternalGameInformationEvent,
    SetPlayerNameEvent,
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# ======= GENERIC =======
class QuitGame(Command):
    def __init__(self) -> None:
        super().__init__("Exit from the game")
        self.events = [QuitGameEvent()]


# ======= GAME STATE SYNC =======
class InitiateGame(Command):
    def __init__(self, game_data: "GameData") -> None:
        super().__init__(f"Locally initializing game {game_data.id}")
        self.events = [
            PlaySoundEvent("start_game"),
            InitiateGameEvent(
                game_data
            ),  # Event to be picked up by the game event handler
            SetInternalGameInformationEvent(game_data.id),
        ]


class SetPlayerName(Command):
    def __init__(self, name: str) -> None:
        super().__init__("Setting player name")
        self.events = [
            SetPlayerNameEvent(name),
        ]


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameCommand(Command):
    def __init__(self, player_id: "UUID") -> None:
        super().__init__(f"Player {player_id} created a game")
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
    def __init__(self, player_id: "UUID") -> None:
        super().__init__(f"Player {player_id} joined the game")
        self.events = [
            PlayerJoinedInGameEvent(
                player_id
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class PlayerWinsInGameCommand(Command):
    def __init__(self, player_id: "UUID") -> None:
        super().__init__(f"Player {player_id} wins the game")
        self.events = [
            PlayerWinsInGameEvent(
                player_id
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


# ==== These are network requests
class PingTheServer(Command):
    def __init__(self) -> None:
        super().__init__("Ping the server")
        self.events = [PingNetworkRequestEvent()]
