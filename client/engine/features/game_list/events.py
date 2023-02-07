from typing import TYPE_CHECKING, List

from client.engine.primitives.event import Event, InGameEvent

if TYPE_CHECKING:
    from common.messages import GameListResponseEntry


class UpdateGameListEvent(InGameEvent):
    def __init__(self, games: List["GameListResponseEntry"]):
        super().__init__()
        self.games = games


class GetGameListNetworkRequestEvent(Event):
    pass


class ErrorGettingGameListEvent(Event):
    pass
