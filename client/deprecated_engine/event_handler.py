import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.external.foundational_wrapper import FoundationalWrapper
from client.engine.features.chat.event_handler import (
    handlers_map as chat_event_handlers,
)
from client.engine.features.game_list.event_handler import (
    handlers_map as game_list_event_handlers,
)
from client.engine.features.game_management.event_handler import (
    handlers_map as game_management_event_handlers,
)
from client.engine.features.network.commands import SendNetworkRequest
from client.engine.features.pieces.event_handler import (
    handlers_map as pieces_event_handlers,
)
from client.engine.features.profile.event_handler import (
    handlers_map as profile_event_handlers,
)
from client.engine.features.synchronization.event_handler import (
    handlers_map as synchronization_event_handlers,
)
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from common.messages import ErrorMessage, PingRequestMessage, PingResponseMessage

from .events import (
    PingNetworkRequestEvent,
    QuitGameEvent,
    SetInternalGameInformationEvent,
    SetPlayerNameEvent,
)

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ======= GENERIC =======
class QuitGameEventHandler(BaseEventHandler[QuitGameEvent]):
    def handle(self, event: "QuitGameEvent") -> None:
        import sys

        FoundationalWrapper.quit()
        """
        Here is where I should probably be safely stopping,
        like:
            while thread_a.is_alive() or thread_b.is_alive():
                time.sleep(0.2)
    
            # The main thread joins the workers to ensure they terminate
            thread_a.join()
            thread_b.join()
        """
        sys.exit()


# ======= GAME STATE SYNC =======
class SetInternalGameInformationEventHandler(
    BaseEventHandler[SetInternalGameInformationEvent]
):
    def handle(self, event: "SetInternalGameInformationEvent") -> None:
        profile_manager = ProfileManager()
        profile_manager.profile.set_game(event.game_id)
        profile_manager.profile.set_game_event_pointer(0)


class SetPlayerNameEventHandler(BaseEventHandler[SetPlayerNameEvent]):
    def handle(self, event: "SetPlayerNameEvent") -> None:
        profile_manager = ProfileManager()
        profile_manager.profile.set_name(event.name)


class PingNetworkRequestEventHandler(BaseEventHandler[PingNetworkRequestEvent]):
    def on_success(self, event, response):
        if isinstance(response, PingResponseMessage):
            logger.info("Ping request OK")
        if isinstance(response, ErrorMessage):
            logger.error(response.__dict__)

    def on_error(self, event):
        logger.error("Error pinging the server")

    def handle(self, event: "PingNetworkRequestEvent") -> None:
        request_data = self._encode()

        SendNetworkRequest(request_data, self.on_success, self.on_error)

    def _encode(self) -> "PingRequestMessage":
        return PingRequestMessage()


common_handlers: Dict[Type["Event"], Any] = {
    QuitGameEvent: QuitGameEventHandler,
    PingNetworkRequestEvent: PingNetworkRequestEventHandler,
    SetInternalGameInformationEvent: SetInternalGameInformationEventHandler,
    SetPlayerNameEvent: SetPlayerNameEventHandler,
}

handlers_map: Dict[Type["Event"], Any] = {
    **common_handlers,
    **chat_event_handlers,
    **pieces_event_handlers,
    **profile_event_handlers,
    **synchronization_event_handlers,
    **game_list_event_handlers,
    **game_management_event_handlers,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
