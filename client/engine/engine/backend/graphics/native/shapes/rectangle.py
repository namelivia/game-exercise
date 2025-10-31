from typing import Any

from engine.backend.foundational_wrapper import FoundationalColor, FoundationalSurface
from engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)


class Rectangle(Shape):
    def __init__(
        self, x: int, y: int, width: int, height: int, color: FoundationalColor = BLACK
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def load(self):
        self.rectangle = FoundationalSurface((self.width, self.height))
        self.rectangle.fill(self.color)

    def render(self, x, y, window: Any, index) -> None:
        dest_x = self.x + x
        dest_y = self.y + y
        if window is not None:
            window.blit(self.rectangle, dest=(dest_x, dest_y))
