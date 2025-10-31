from typing import Any, Dict

import pygame

from ..base import BaseGraphicsBackend


class PygameNativeGraphicsBackend(BaseGraphicsBackend):
    def update_display(self) -> None:
        pygame.display.update()
        return None

    def load_image(self, path: str):
        return pygame.image.load(path)

    def get_new_window(self, width: int, height: int) -> pygame.Surface:
        return pygame.display.set_mode((width, height), pygame.DOUBLEBUF)

    def clear_window(self, window):
        window.fill((0, 0, 0))
