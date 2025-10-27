import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.backend.backend import Backend
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from client.engine.threads import ThreadManager

from .events import QuitGameEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event
    from client.engine.primitives.event_handler import (
        EventHandler as GenericEventHandler,
    )

logger = logging.getLogger(__name__)


class QuitGameEventHandler(BaseEventHandler[QuitGameEvent]):
    def handle(self, event: QuitGameEvent) -> None:
        import sys

        ThreadManager().shutdown()
        Backend.quit()
        sys.exit()


handlers_map: Dict[Type["Event"], Type["GenericEventHandler[Any]"]] = {
    QuitGameEvent: QuitGameEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handler_class: Type["GenericEventHandler[Any]"] = handlers_map[type(event)]
        handler: "GenericEventHandler[Any]" = handler_class()
        handler.handle(event)
