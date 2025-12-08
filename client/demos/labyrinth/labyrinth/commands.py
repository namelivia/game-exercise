from engine.api import Command

from .events import SetCustomCursorEvent


class SetCustomCursor(Command):
    def __init__(self, key) -> None:
        super().__init__(f"Set the custom cursor {key}")
        self.events = [SetCustomCursorEvent(key)]
