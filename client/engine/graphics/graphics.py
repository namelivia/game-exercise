from typing import TYPE_CHECKING

from client.engine.backend.graphics.graphics import GraphicsBackend

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


class Graphics:
    def __init__(self) -> None:
        self.window = GraphicsBackend.get().get_new_window(640, 480)

    def render(self, screen: "Screen") -> None:
        self.window.fill((255, 255, 255))
        screen.render(self.window)
        GraphicsBackend.get().update_display()
        return None
