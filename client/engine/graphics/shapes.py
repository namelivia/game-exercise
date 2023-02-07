from typing import Any, Tuple

import pygame

from client.engine.primitives.shape import Shape

from .sprite import Sprite

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)


class Text(Shape):
    def __init__(self, message: str, x: int, y: int, color: pygame.Color = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message: str) -> None:
        self.message = message


class Rectangle(Shape):
    def __init__(
        self, x: int, y: int, width: int, height: int, color: pygame.Color = BLACK
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:  # TODO: only if pygame
            rectangle = pygame.Surface((self.width, self.height))
            rectangle.fill(self.color)
            rectangle.set_alpha(128)  # TODO: Alpha could be passed
            window.blit(rectangle, dest=(self.x, self.y))


class SmallText(Shape):
    def __init__(self, message: str, x: int, y: int, color: pygame.Color = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message: str) -> None:
        self.message = message


class Image(Shape):
    def __init__(self, path: str, x: int, y: int):
        super().__init__(x, y)
        self.image = pygame.image.load(path)

    def render(self, window: Any) -> None:
        if window is not None:  # TODO: only if pygame
            window.blit(self.image, dest=(self.x, self.y))


class Animation(Shape):
    def __init__(self, folder: str, x: int, y: int, initial_frame: int = 0):
        super().__init__(x, y)
        self.sprite_group = pygame.sprite.Group()
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
        if window is not None:  # TODO: only if pygame
            self.sprite_group.draw(window)
