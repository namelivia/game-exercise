from client.primitives.event_handler import EventHandler
from .events import (
    QuitGameEvent,
)

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


class QuitGameEventHandler(EventHandler):
    def handle(self, event, client_state, graphics):
        import pygame  # This is pygame dependent
        import sys
        pygame.quit()
        sys.exit()


handlers_map = {
    QuitGameEvent: QuitGameEventHandler,
}


class EventHandler():

    def handle(self, event, client_state, graphics):
        try:
            handlers_map[type(event)]().handle(event, client_state, graphics)
        except KeyError:
            pass  # Unhandled event
