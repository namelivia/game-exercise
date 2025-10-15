from typing import TYPE_CHECKING

from client.engine.features.render.temp import create_render_from_screen
from client.engine.primitives.command import Command
from client.engine.primitives.screen import Screen

from .events import StartRenderingEvent


class StartRendering(Command):
    def __init__(self, screen: "Screen") -> None:
        super().__init__(f"Start rendering the screen")
        self.queue = "render"
        self.events = [
            StartRenderingEvent(create_render_from_screen(screen)),
        ]
