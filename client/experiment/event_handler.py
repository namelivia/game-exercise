from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.general_state.current_screen import CurrentScreen
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler

from .events import ScreenTransitionEvent
from .screens.main.main import MainScreen

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class ScreenTransitionEventHandler(BaseEventHandler[ScreenTransitionEvent]):
    def handle(self, event: ScreenTransitionEvent) -> None:
        # Could I just push the instances to the queue?
        if event.dest_screen == "main":
            CurrentScreen().set_current_screen(MainScreen())


handlers_map: Dict[Type["Event"], Any] = {
    ScreenTransitionEvent: ScreenTransitionEventHandler
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
