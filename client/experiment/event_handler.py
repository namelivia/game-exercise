from typing import TYPE_CHECKING

from client.engine.primitives.event_handler import EventHandler as BaseEventHandler

from .events import ScreenTransitionEvent
from .screens.main.main import MainScreen

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class ScreenTransitionEventHandler(BaseEventHandler):
    def handle(self, event: ScreenTransitionEvent, client_state: "ClientState") -> None:
        # Could I just push the instances to the queue?
        if event.dest_screen == "main":
            client_state.set_current_screen(MainScreen(client_state))


handlers_map = {ScreenTransitionEvent: ScreenTransitionEventHandler}


class EventHandler(BaseEventHandler):
    def handle(self, event: "Event", client_state: "ClientState") -> None:
        handlers_map[type(event)]().handle(event, client_state)
