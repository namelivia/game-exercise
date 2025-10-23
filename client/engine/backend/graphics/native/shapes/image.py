from typing import Any

from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)


class Image(Shape):
    def __init__(self, path: str, x: int, y: int):
        super().__init__(x, y)
        self.path = path

    def load(self):

        self.image = GraphicsBackend().get().load_image(self.path)

    def render(self, x, y, window: Any) -> None:
        dest_x = x + self.x
        dest_y = y + self.y
        if window is not None:
            window.blit(self.image, dest=(dest_x, dest_y))

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_width(self) -> int:
        return self.image.get_width()

    def get_height(self) -> int:
        return self.image.get_height()
