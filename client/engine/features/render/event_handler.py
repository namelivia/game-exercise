import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.primitives.event_handler import EventHandler

from .events import StartRenderingEvent
from .state import State

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class StartRenderingEventHandler(EventHandler[StartRenderingEvent]):
    def handle(self, event: "StartRenderingEvent") -> None:
        event.screen.load()
        State().start_rendering()


handlers_map: Dict[Type["Event"], Any] = {
    StartRenderingEvent: StartRenderingEventHandler
}
