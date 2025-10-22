from typing import Any

from client.engine.backend.foundational_wrapper import (
    FoundationalColor,
    FoundationalSurface,
)
from client.engine.primitives.shape import Shape

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

    def render(self, window: Any) -> None:
        if window is not None:
            window.blit(self.rectangle, dest=(self.x, self.y))
