from client.engine.primitives.event import Event, InGameEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.game_data import GameData

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


# ======= GENERIC =======
class QuitGameEvent(Event):
    pass


# ======= GAME STATE SYNC =======
class InitiateGameEvent(Event):
    def __init__(self, game_data: "GameData"):
        super().__init__()
        self.game_data = game_data


class SetInternalGameInformationEvent(Event):
    def __init__(self, game_id: str):
        super().__init__()
        self.game_id = game_id


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameEvent(InGameEvent):
    def __init__(self, player_id: str):
        super().__init__()
        self.player_id = player_id


class PlayerJoinedInGameEvent(InGameEvent):
    def __init__(self, player_id: str):
        super().__init__()
        self.player_id = player_id


class PlayerWinsInGameEvent(InGameEvent):
    def __init__(self, player_id: str):
        super().__init__()
        self.player_id = player_id


# These are network requests
class PingNetworkRequestEvent(Event):
    pass


class SetPlayerNameEvent(Event):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
