from client.engine.primitives.event import Event
from client.engine.primitives.screen import Screen


class StartRenderingEvent(Event):
    def __init__(self, screen: Screen):
        super().__init__()
        self.screen = screen
