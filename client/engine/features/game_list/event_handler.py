import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.network.channel import Channel
from client.engine.primitives.event_handler import EventHandler
from common.messages import (
    ErrorMessage,
    GameListRequestMessage,
    GameListResponseMessage,
)

from .commands import ErrorGettingGameList, UpdateGameList
from .events import GetGameListNetworkRequestEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class ErrorGettingGameListEventHandler(EventHandler["Event"]):
    pass


class GetGameListNetworkRequestEventHandler(
    EventHandler[GetGameListNetworkRequestEvent]
):
    def handle(self, event: "GetGameListNetworkRequestEvent") -> None:
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameListResponseMessage):
                UpdateGameList(response.games).execute()
            if isinstance(response, ErrorMessage):
                ErrorGettingGameList().execute()
                logger.info(response.__dict__)
        else:
            ErrorGettingGameList().execute()
            logger.error("Error retrieving the game list from the server")

    def _encode(self) -> "GameListRequestMessage":
        return GameListRequestMessage()


handlers_map: Dict[Type["Event"], Any] = {
    GetGameListNetworkRequestEvent: GetGameListNetworkRequestEventHandler
}
