from client.engine.primitives.command import Command
from .events import (
    UpdateGameListEvent,
    GetGameListNetworkRequestEvent,
    ErrorGettingGameListEvent,
)


class UpdateGameList(Command):
    def __init__(self, profile, queue, games):
        super().__init__(profile, queue, "Updating game list")
        self.events = [UpdateGameListEvent(games)]


class GetGameList(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Get Game List")
        self.events = [GetGameListNetworkRequestEvent()]


class ErrorGettingGameList(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Error Getting Game List")
        self.events = [ErrorGettingGameListEvent()]
