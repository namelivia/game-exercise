from typing import TYPE_CHECKING, Any, Dict, Type

from engine.primitives.event_handler import EventHandler

from .channel import Channel
from .events import NetworkRequestEvent

if TYPE_CHECKING:
    from engine.primitives.event import Event


class NetworkRequestEventHandler(EventHandler[NetworkRequestEvent]):
    def handle(self, event: "NetworkRequestEvent") -> None:
        response = Channel.send_command(event.data)
        if response is not None:
            event.on_success_callback(event, response)
        else:
            event.on_error_callback(event)


handlers_map: Dict[Type["Event"], Any] = {
    NetworkRequestEvent: NetworkRequestEventHandler,
}
