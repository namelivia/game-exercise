from typing import TYPE_CHECKING, List

from client.engine.primitives.command import Command

from .events import (
    ErrorGettingGameListEvent,
    GetGameListNetworkRequestEvent,
    UpdateGameListEvent,
)

if TYPE_CHECKING:
    from common.messages import GameListResponseEntry


class UpdateGameList(Command):
    def __init__(self, games: List["GameListResponseEntry"]) -> None:
        super().__init__("Updating game list")
        self.events = [UpdateGameListEvent(games)]


class GetGameList(Command):
    def __init__(self) -> None:
        super().__init__("Get Game List")
        self.events = [GetGameListNetworkRequestEvent()]


class ErrorGettingGameList(Command):
    def __init__(self) -> None:
        super().__init__("Error Getting Game List")
        self.events = [ErrorGettingGameListEvent()]
