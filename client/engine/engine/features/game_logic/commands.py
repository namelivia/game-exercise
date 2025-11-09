from typing import TYPE_CHECKING, Type

from engine.primitives.command import Command
from engine.primitives.screen import Screen

from .events import ChangeCursorEvent, ScreenTransitionEvent


class ChangeCursor(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"Setting cursor to {key}")
        self.queue = "game_logic"
        self.events = [
            ChangeCursorEvent(key),
        ]


class ScreenTransition(Command):
    def __init__(self, dest_screen: Type[Screen]) -> None:
        super().__init__(f"Transitioning to another screen")
        self.queue = "game_logic"
        self.events = [
            ScreenTransitionEvent(dest_screen()),
        ]
