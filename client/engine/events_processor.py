import logging
from typing import TYPE_CHECKING, List

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from client.engine.primitives.event import Event
    from client.engine.primitives.event_handler import EventHandler


class EventsProcessor:
    def __init__(self, event_handlers: List["EventHandler[Event]"]):
        self.event_handlers = event_handlers  # Initial list of event handlers

    def add_event_handler(self, event_handler: "EventHandler[Event]") -> None:
        self.event_handlers.append(event_handler)

    def handle(self, event: "Event") -> None:
        if event is None:
            return
        handled = False
        for event_handler in self.event_handlers:
            try:
                event_handler.handle(event)
                handled = True
            except KeyError:
                pass
        if not handled:
            logger.error(f"[ERROR] Unhandled event {event.__class__.__name__}")
