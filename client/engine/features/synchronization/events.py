from client.engine.primitives.event import Event
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


class UpdateGameEvent(Event):
    def __init__(self, events: List["Event"]):
        super().__init__()
        self.events = events


class RefreshGameStatusEvent(Event):
    def __init__(self, game_id: "UUID", pointer: int):
        super().__init__()
        self.game_id = game_id
        self.pointer = pointer


class RefreshGameStatusNetworkRequestEvent(Event):
    def __init__(self, game_id: "UUID", pointer: int):
        super().__init__()
        self.game_id = game_id
        self.pointer = pointer
