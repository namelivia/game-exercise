# TODO: Temporary location
from typing import TYPE_CHECKING, Any

import numpy

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


class VisualRegression:
    @staticmethod
    def _render_surface(screen: "Screen") -> Any:
        """
        Renders a new surface to be compared
        """
        ui_elements = screen.get_ui_elements()
        import pygame

        pygame.init()
        surface = pygame.Surface((640, 480))
        surface.fill((255, 255, 255))  # Clear the surface
        for ui_element in ui_elements:
            ui_element.render(surface)
        return surface

    @staticmethod
    def assert_matches_snapshot(screen: "Screen", snapshot_key: str) -> None:
        import pygame

        new_surface = VisualRegression._render_surface(screen)
        # Convert matches the image pixel depth to the original surface
        screenshot = pygame.image.load(snapshot_key).convert(new_surface)
        new_array = pygame.surfarray.array2d(new_surface)
        screenshot_array = pygame.surfarray.array2d(screenshot)

        numpy.testing.assert_array_equal(new_array, screenshot_array)

    @staticmethod
    def generate_snapshot(screen: "Screen", snapshot_key: str) -> None:
        # Used to generate snapshots
        import pygame

        new_surface = VisualRegression._render_surface(screen)
        pygame.image.save(new_surface, snapshot_key)
