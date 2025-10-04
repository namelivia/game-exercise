from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import ChangeCursorEvent


class ChangeCursor(Command):
    def __init__(self, key: str) -> None:
        super().__init__(f"Settings cursor to {key}")
        self.queue = "game_logic"
        self.events = [
            ChangeCursorEvent(key),
        ]
