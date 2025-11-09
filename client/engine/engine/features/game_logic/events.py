from engine.primitives.event import Event
from engine.primitives.screen import Screen


class ChangeCursorEvent(Event):
    def __init__(self, key: str):
        super().__init__()
        self.key = key


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen: Screen):
        super().__init__()
        self.dest_screen = dest_screen
