from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


class Graphics:
    def __init__(self, uses_pygame: bool) -> None:
        self.uses_pygame = uses_pygame
        if uses_pygame:
            import pygame

            self.window = pygame.display.set_mode((640, 480))

    def render(self, screen: "Screen") -> None:
        ui_elements = screen.get_ui_elements()
        import pygame

        if self.uses_pygame:
            self.window.fill((255, 255, 255))  # Clear the window (only pygame)
        for ui_element in ui_elements:
            ui_element.render(self.window)
        if self.uses_pygame:
            pygame.display.update()  # Only pygame
        return None
