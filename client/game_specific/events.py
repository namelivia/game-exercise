from abc import ABC


class Event(ABC):
    pass


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen):
        super().__init__()
        self.dest_screen = dest_screen


class UserTypedEvent(Event):
    def __init__(self, key):
        super().__init__()
        self.key = key
