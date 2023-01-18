from client.engine.primitives.command import Command
from .events import (
    RefreshGameStatusNetworkRequestEvent,
    RefreshGameStatusEvent,
    UpdateGameEvent,
)


class RefreshGameStatus(Command):
    def __init__(self, profile, queue, game_id, pointer):
        super().__init__(
            profile, queue, f"Refresh game status {game_id} pointer {pointer}"
        )
        self.events = [RefreshGameStatusNetworkRequestEvent(game_id, pointer)]


class RequestGameStatus(Command):
    def __init__(self, profile, queue, game_id, pointer):
        super().__init__(
            profile,
            queue,
            f"Request refreshing the status of game {game_id} pointer {pointer}",
        )
        self.events = [RefreshGameStatusEvent(game_id, pointer)]


class ProcessServerEvents(Command):
    def __init__(self, profile, queue, events):
        super().__init__(
            profile, queue, f"Processing {len(events)} unprocessed server events"
        )
        self.events = events


class UpdateGame(Command):
    def __init__(self, profile, queue, events):
        super().__init__(profile, queue, "Locally updating game")
        self.events = [UpdateGameEvent(events)]
