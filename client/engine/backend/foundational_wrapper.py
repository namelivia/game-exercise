from typing import Any

import pygame
from PIL import Image


class FoundationalSprite(pygame.sprite.Sprite):
    pass


class FoundationalColor(pygame.Color):
    pass


# This won't work on opengl
class FoundationalSurface(pygame.Surface):
    pass


class FoundationalClock:
    def __init__(self):
        self._clock = pygame.time.Clock()

    def tick(self, framerate: int = 0) -> int:
        return self._clock.tick(framerate)


class FoundationalWrapper:

    @staticmethod
    def get_clock_ticks() -> int:
        return int(pygame.time.get_ticks())

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        # Only for Openg
        return Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        # return pygame.image.load(path)
