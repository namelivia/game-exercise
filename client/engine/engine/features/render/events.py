from engine.primitives.event import Event

from .screen import ScreenRender


class RefreshRenderScreenEvent(Event):
    def __init__(self, screen: ScreenRender):
        super().__init__()
        self.screen = screen
