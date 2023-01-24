from typing import TYPE_CHECKING
import logging
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from .events import (
    QuitGameEvent,
    SetInternalGameInformationEvent,
    PingNetworkRequestEvent,
    SetPlayerNameEvent,
)

from common.messages import (
    ErrorMessage,
    PingRequestMessage,
    PingResponseMessage,
)
from client.engine.network.channel import Channel
from client.engine.features.chat.event_handler import (
    handlers_map as chat_event_handlers,
)
from client.engine.features.pieces.event_handler import (
    handlers_map as pieces_event_handlers,
)
from client.engine.features.profile.event_handler import (
    handlers_map as profile_event_handlers,
)
from client.engine.features.sound.event_handler import (
    handlers_map as sound_event_handlers,
)
from client.engine.features.synchronization.event_handler import (
    handlers_map as synchronization_event_handlers,
)
from client.engine.features.game_list.event_handler import (
    handlers_map as game_list_event_handlers,
)
from client.engine.features.game_management.event_handler import (
    handlers_map as game_management_event_handlers,
)

if TYPE_CHECKING:
    from client.engine.client_state import ClientState
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ======= GENERIC =======
class QuitGameEventHandler(BaseEventHandler):
    def handle(self, event: "QuitGameEvent", client_state: "ClientState") -> None:
        import pygame  # This is pygame dependent
        import sys

        pygame.quit()
        sys.exit()


# ======= GAME STATE SYNC =======
class SetInternalGameInformationEventHandler(BaseEventHandler):
    def handle(
        self, event: "SetInternalGameInformationEvent", client_state: "ClientState"
    ) -> None:
        client_state.profile.set_game(event.game_id)
        client_state.profile.set_game_event_pointer(0)


class SetPlayerNameEventHandler(BaseEventHandler):
    def handle(self, event: "SetPlayerNameEvent", client_state: "ClientState") -> None:
        client_state.profile.set_name(event.name)


class PingNetworkRequestEventHandler(BaseEventHandler):
    def handle(self, event, client_state: "ClientState") -> None:
        request_data = self._encode()

        response = Channel.send_command(request_data)
        if response is not None:
            if isinstance(response, PingResponseMessage):
                logger.info("Ping request OK")
            if isinstance(response, ErrorMessage):
                logger.error(response.__dict__)
        else:
            logger.error("Error pinging the server")

    def _encode(self):
        return PingRequestMessage()


common_handlers = {
    QuitGameEvent: QuitGameEventHandler,
    PingNetworkRequestEvent: PingNetworkRequestEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    SetPlayerNameEvent: SetPlayerNameEventHandler,
}

handlers_map = {
    **common_handlers,
    **chat_event_handlers,
    **pieces_event_handlers,
    **profile_event_handlers,
    **sound_event_handlers,
    **synchronization_event_handlers,
    **game_list_event_handlers,
    **game_management_event_handlers,
}


class EventHandler:
    def handle(self, event: "Event", client_state: "ClientState") -> None:
        handlers_map[type(event)]().handle(event, client_state)
