import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from engine.backend.backend import Backend
from engine.primitives.event_handler import EventHandler as BaseEventHandler
from engine.threading.manager import ThreadManager

from .events import QuitGameEvent

if TYPE_CHECKING:
    from engine.primitives.event import Event

logger = logging.getLogger(__name__)


class QuitGameEventHandler(BaseEventHandler[QuitGameEvent]):
    def handle(self, event: "QuitGameEvent") -> None:
        import sys

        ThreadManager().shutdown()
        Backend.quit()
        sys.exit()


handlers_map: Dict[Type["Event"], Any] = {
    QuitGameEvent: QuitGameEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
