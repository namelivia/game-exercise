from engine.primitives.event import Event

from .screen import ScreenRender


class StartRenderingEvent(Event):
    def __init__(self, screen: ScreenRender):
        super().__init__()
        self.screen = screen
