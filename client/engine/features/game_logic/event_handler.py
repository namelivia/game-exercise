import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.backend.graphics import PygameNativeGraphicsBackend
from client.engine.primitives.event_handler import EventHandler

from .events import ChangeCursorEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class ChangeCursorEventHandler(EventHandler[ChangeCursorEvent]):
    def handle(self, event: "ChangeCursorEvent") -> None:
        PygameNativeGraphicsBackend.set_mouse_cursor(event.key)


handlers_map: Dict[Type["Event"], Any] = {
    ChangeCursorEvent: ChangeCursorEventHandler,
}
