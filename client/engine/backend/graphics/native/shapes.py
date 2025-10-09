from typing import Any, Tuple

from client.engine.backend.fonts.manager import FontManager
from client.engine.backend.foundational_wrapper import (
    FoundationalColor,
    FoundationalSurface,
)
from client.engine.primitives.shape import Shape

from .sprite import Sprite

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)


class Text(Shape):
    def __init__(self, message: str, x: int, y: int, color: FoundationalColor = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:
            font = FontManager.get_font(FontManager.get_default_font(), 24)
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message: str) -> None:
        self.message = message


class Rectangle(Shape):
    def __init__(
        self, x: int, y: int, width: int, height: int, color: FoundationalColor = BLACK
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:
            rectangle = FoundationalSurface((self.width, self.height))
            rectangle.fill(self.color)
            rectangle.set_alpha(128)  # TODO: Alpha could be passed
            window.blit(rectangle, dest=(self.x, self.y))


class Image(Shape):
    def __init__(self, path: str, x: int, y: int):
        super().__init__(x, y)
        # Circular import
        from client.engine.backend.graphics.graphics import GraphicsBackend

        self.image = GraphicsBackend().get().load_image(path)

    def render(self, window: Any) -> None:
        if window is not None:
            window.blit(self.image, dest=(self.x, self.y))

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_width(self) -> int:
        return self.image.get_width()

    def get_height(self) -> int:
        return self.image.get_height()


class Animation(Shape):
    def __init__(self, folder: str, x: int, y: int, initial_frame: int = 0):
        super().__init__(x, y)
        # Circular import
        from client.engine.backend.graphics import GraphicsBackend

        self.sprite_group = GraphicsBackend.sprite_group()
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
