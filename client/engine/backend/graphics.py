from typing import Any

import pygame


class GraphicsBackend:

    @staticmethod
    def update_display() -> None:
        pygame.display.update()
        return None

    @staticmethod
    def get_new_window(width: int, height: int) -> pygame.Surface:
        return pygame.display.set_mode((width, height))

    @staticmethod
    def set_mouse_cursor(new_cursor: str) -> None:
        cursors = {
            "ARROW": pygame.SYSTEM_CURSOR_ARROW,
            "IBEAM": pygame.SYSTEM_CURSOR_IBEAM,
            "WAIT": pygame.SYSTEM_CURSOR_WAIT,
            "CROSSHAIR": pygame.SYSTEM_CURSOR_CROSSHAIR,
            "WAITARROW": pygame.SYSTEM_CURSOR_WAITARROW,
            "SIZENWSE": pygame.SYSTEM_CURSOR_SIZENWSE,
            "SIZENESW": pygame.SYSTEM_CURSOR_SIZENESW,
            "SIZEWE": pygame.SYSTEM_CURSOR_SIZEWE,
            "SIZENS": pygame.SYSTEM_CURSOR_SIZENS,
            "SIZEALL": pygame.SYSTEM_CURSOR_SIZEALL,
            "NO": pygame.SYSTEM_CURSOR_NO,
            "HAND": pygame.SYSTEM_CURSOR_HAND,
        }
        try:
            pygame.mouse.set_cursor(cursors[new_cursor])
        except KeyError:
            pass
        return None

    # TODO: I had to add Any here as I could not find a way to type hint this
    @staticmethod
    def sprite_group() -> Any:
        return pygame.sprite.Group()

    @staticmethod
    def get_default_font() -> str:
        return pygame.font.get_default_font()

    @staticmethod
    def get_font(font: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font, size)
