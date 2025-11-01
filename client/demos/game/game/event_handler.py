from typing import TYPE_CHECKING, Any, Dict, Type

from engine.current_screen import CurrentScreen
from engine.primitives.event_handler import EventHandler as BaseEventHandler

from .events import ScreenTransitionEvent
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby

if TYPE_CHECKING:
    from engine.primitives.event import Event

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class ScreenTransitionEventHandler(BaseEventHandler[ScreenTransitionEvent]):
    def handle(self, event: ScreenTransitionEvent) -> None:
        current_screen = CurrentScreen()
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            current_screen.set_current_screen(Intro())
        if event.dest_screen == "lobby":
            current_screen.set_current_screen(Lobby())


handlers_map: Dict[Type["Event"], Any] = {
    ScreenTransitionEvent: ScreenTransitionEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
