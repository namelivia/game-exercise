import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.features.network.channel import Channel
from client.engine.primitives.event_handler import EventHandler

from .events import NetworkRequestEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class NetworkRequestEventHandler(EventHandler[NetworkRequestEvent]):
    def handle(self, event: "NetworkRequestEvent") -> None:
        response = Channel.send_command(event.data)
        if response is not None:
            event.on_success_callback(response)
        else:
            event.on_error_callback(response)


handlers_map: Dict[Type["Event"], Any] = {
    NetworkRequestEvent: NetworkRequestEventHandler,
}
