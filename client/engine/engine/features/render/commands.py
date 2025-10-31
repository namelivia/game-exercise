from typing import TYPE_CHECKING

from engine.primitives.command import Command

from .screen import create_render_from_screen

if TYPE_CHECKING:
    from engine.primitives.screen import Screen

from .events import StartRenderingEvent


class StartRendering(Command):
    def __init__(self, screen: "Screen") -> None:
        super().__init__(f"Start rendering the screen")
        self.queue = "render"
        self.events = [
            StartRenderingEvent(create_render_from_screen(screen)),
        ]
