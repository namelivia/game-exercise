from client.engine.features.render.temp import ScreenRender
from client.engine.primitives.event import Event


class StartRenderingEvent(Event):
    def __init__(self, screen: ScreenRender):
        super().__init__()
        self.screen = screen
