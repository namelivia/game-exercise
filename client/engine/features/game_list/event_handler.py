import logging
from typing import TYPE_CHECKING
from client.engine.primitives.event_handler import EventHandler
from client.engine.network.channel import Channel
from .commands import (
    UpdateGameList,
    ErrorGettingGameList,
)
from .events import (
    GetGameListNetworkRequestEvent,
)
from common.messages import (
    ErrorMessage,
    GameListRequestMessage,
    GameListResponseMessage,
)

if TYPE_CHECKING:
    from client.engine.client_state import ClientState


logger = logging.getLogger(__name__)


class GetGameListNetworkRequestEventHandler(EventHandler):
    def handle(
        self, event: "GetGameListNetworkRequestEvent", client_state: "ClientState"
    ):
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, GameListResponseMessage):
                UpdateGameList(
                    client_state.profile, client_state.queue, response.games
                ).execute()
            if isinstance(response, ErrorMessage):
                ErrorGettingGameList(
                    client_state.profile,
                    client_state.queue,
                ).execute()
                logger.info(response.__dict__)
        else:
            ErrorGettingGameList(
                client_state.profile,
                client_state.queue,
            ).execute()
            logger.error("Error retrieving the game list from the server")

    def _encode(self):
        return GameListRequestMessage()


handlers_map = {
    GetGameListNetworkRequestEvent: GetGameListNetworkRequestEventHandler,
}
