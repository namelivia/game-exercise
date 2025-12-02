from typing import TYPE_CHECKING

from engine.primitives.command import Command

from .screen import create_render_from_screen

if TYPE_CHECKING:
    from engine.primitives.screen import Screen

from .events import RefreshRenderScreenEvent


class RefreshRenderScreen(Command):
    def __init__(self, screen: "Screen") -> None:
        super().__init__(f"Refreshing the render for the screen")
        self.queue = "render"
        self.events = [
            RefreshRenderScreenEvent(create_render_from_screen(screen)),
        ]
