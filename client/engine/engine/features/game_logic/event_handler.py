import logging
from typing import TYPE_CHECKING, Any, Dict, Type

from engine.current_screen import CurrentScreen
from engine.primitives.event_handler import EventHandler as BaseEventHandler

from .backend.cursor.pygame_cursor import PygameCursor
from .events import ChangeCursorEvent, ScreenTransitionEvent

if TYPE_CHECKING:
    from engine.primitives.event import Event

logger = logging.getLogger(__name__)


class ChangeCursorEventHandler(BaseEventHandler[ChangeCursorEvent]):
    def handle(self, event: "ChangeCursorEvent") -> None:
        PygameCursor().set_mouse_cursor(event.key)


class ScreenTransitionEventHandler(BaseEventHandler[ScreenTransitionEvent]):
    def handle(self, event: ScreenTransitionEvent) -> None:
        CurrentScreen().set_current_screen(event.dest_screen)


handlers_map: Dict[Type["Event"], Any] = {
    ChangeCursorEvent: ChangeCursorEventHandler,
    ScreenTransitionEvent: ScreenTransitionEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
