import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.backend.foundational_wrapper import FoundationalWrapper
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler

from .events import QuitGameEvent

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


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


handlers_map: Dict[Type["Event"], Any] = {
    QuitGameEvent: QuitGameEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
