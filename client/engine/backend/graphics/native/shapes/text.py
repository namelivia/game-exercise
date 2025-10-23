from typing import Any

from client.engine.backend.fonts.manager import FontManager
from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)


class Text(Shape):
    def __init__(self, message: str, x: int, y: int, color: FoundationalColor = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def load(self):
        font = FontManager.get().get_font(FontManager.get().get_default_font(), 24)
        self.surface = font.render(self.message, True, self.color)

    def render(self, x, y, window: Any) -> None:
        dest_x = self.x + x
        dest_y = self.y + y
        if window is not None:
            window.blit(self.surface, dest=(dest_x, dest_y))

    def set_message(self, message: str) -> None:
        self.message = message
