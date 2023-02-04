from typing import TYPE_CHECKING

# TODO: Maybe then this primitive should be at a higher level
from client.engine.primitives.event import Event

if TYPE_CHECKING:
    from uuid import UUID


class GameCreated(Event):
    def __init__(self, player_id: "UUID"):
        super().__init__()
        self.player_id = player_id


class PlayerJoined(Event):
    def __init__(self, player_id: "UUID"):
        super().__init__()
        self.player_id = player_id


class PlayerPlacedSymbol(Event):
    def __init__(self, event_id: "UUID", player_id: "UUID", position: int):
        super().__init__()
        self.event_id = event_id
        self.player_id = player_id
        self.position = position


class ChatMessageEvent(Event):
    def __init__(self, event_id: "UUID", player_id: "UUID", message: str):
        super().__init__()
        self.event_id = event_id
        self.player_id = player_id
        self.message = message


class PlayerWins(Event):
    def __init__(self, player_id: "UUID"):
        super().__init__()
        self.player_id = player_id
