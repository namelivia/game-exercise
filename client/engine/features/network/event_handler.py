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
        Channel.send_command(event.data)


handlers_map: Dict[Type["Event"], Any] = {
    NetworkRequestEvent: NetworkRequestEventHandler,
}
