from typing import TYPE_CHECKING, List

from client.engine.primitives.command import Command

from .events import (
    RefreshGameStatusEvent,
    RefreshGameStatusNetworkRequestEvent,
    UpdateGameEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue
    from client.engine.primitives.event import Event


class RefreshGameStatus(Command):
    def __init__(
        self, profile: "Profile", queue: "Queue", game_id: "UUID", pointer: int
    ):
        super().__init__(
            profile, queue, f"Refresh game status {game_id} pointer {pointer}"
        )
        self.events = [RefreshGameStatusNetworkRequestEvent(game_id, pointer)]


class RequestGameStatus(Command):
    def __init__(
        self, profile: "Profile", queue: "Queue", game_id: "UUID", pointer: int
    ):
        super().__init__(
            profile,
            queue,
            f"Request refreshing the status of game {game_id} pointer {pointer}",
        )
        self.events = [RefreshGameStatusEvent(game_id, pointer)]


class ProcessServerEvents(Command):
    def __init__(self, profile: "Profile", queue: "Queue", events: List["Event"]):
        super().__init__(
            profile, queue, f"Processing {len(events)} unprocessed server events"
        )
        self.events = events


class UpdateGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue", events: List["Event"]):
        super().__init__(profile, queue, "Locally updating game")
        self.events = [UpdateGameEvent(events)]
