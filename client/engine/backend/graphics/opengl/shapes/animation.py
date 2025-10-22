from typing import Any

from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.primitives.shape import Shape

from .sprite import Sprite

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)


class Animation(Shape):
    def __init__(self, folder: str, x: int, y: int, initial_frame: int = 0):
        super().__init__(x, y)
        self.sprite_group = GraphicsBackend.get().sprite_group()
        self.animation = Sprite(folder, x, y, initial_frame)
        self.sprite_group.add(self.animation)

    def set_x(self, x: int) -> None:
        super().set_x(x)
        self.animation.set_x(x)

    def set_y(self, y: int) -> None:
        super().set_y(y)
        self.animation.set_y(y)

    def update(self) -> None:
        self.sprite_group.update()  # Calls update on every sprite on the group

    def render(self, window: Any) -> None:
        if window is not None:
            self.sprite_group.draw(window)

    def get_x(self) -> int:
        return self.animation.get_x()

    def get_y(self) -> int:
        return self.animation.get_y()

    def get_width(self) -> int:
        return self.animation.get_width()

    def get_height(self) -> int:
        return self.animation.get_width()
