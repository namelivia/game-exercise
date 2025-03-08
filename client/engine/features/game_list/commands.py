from typing import TYPE_CHECKING, List

from client.engine.primitives.command import Command

from .events import (
    ErrorGettingGameListEvent,
    GetGameListNetworkRequestEvent,
    UpdateGameListEvent,
)

if TYPE_CHECKING:
    from client.engine.general_state.queue import Queue
    from common.messages import GameListResponseEntry


class UpdateGameList(Command):
    def __init__(self, queue: "Queue", games: List["GameListResponseEntry"]):
        super().__init__(queue, "Updating game list")
        self.events = [UpdateGameListEvent(games)]


class GetGameList(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Get Game List")
        self.events = [GetGameListNetworkRequestEvent()]


class ErrorGettingGameList(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Error Getting Game List")
        self.events = [ErrorGettingGameListEvent()]
