from typing import TYPE_CHECKING, List

from client.engine.primitives.command import Command

from .events import (
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    UpdateGameEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.primitives.event import Event


class RefreshGameStatus(Command):
    def __init__(self, game_id: "UUID", pointer: int) -> None:
        super().__init__(f"Refresh game status {game_id} pointer {pointer}")
        self.events = [RefreshGameStatusNetworkRequestEvent(game_id, pointer)]


class RequestGameStatus(Command):
    def __init__(self, game_id: "UUID", pointer: int) -> None:
        super().__init__(
            f"Request refreshing the status of game {game_id} pointer {pointer}",
        )
        self.events = [RefreshGameStatusEvent(game_id, pointer)]


class ProcessServerEvents(Command):
    def __init__(self, events: List["Event"]) -> None:
        super().__init__(f"Processing {len(events)} unprocessed server events")
        self.events = events


class UpdateGame(Command):
    def __init__(self, events: List["Event"]) -> None:
        super().__init__("Locally updating game")
        self.events = [UpdateGameEvent(events)]
