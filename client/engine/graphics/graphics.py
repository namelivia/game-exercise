from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


class Graphics:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((640, 480))

    def render(self, screen: "Screen") -> None:
        ui_elements = screen.get_ui_elements()
        self.window.fill((255, 255, 255))  # Clear the window (only pygame)
        for ui_element in ui_elements:
            ui_element.render(self.window)
        pygame.display.update()  # Only pygame
        return None
