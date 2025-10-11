from typing import TYPE_CHECKING

from client.engine.primitives.command import Command
from client.engine.primitives.screen import Screen

from .events import StartRenderingEvent


class StartRendering(Command):
    def __init__(self, screen: "Screen") -> None:
        super().__init__(f"Start rendering the screen")
        self.queue = "render"
        self.events = [
            StartRenderingEvent(screen),
        ]
