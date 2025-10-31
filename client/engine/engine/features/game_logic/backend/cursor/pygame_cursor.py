from typing import Any, Dict

import pygame

from .basecursor import BaseCursor


# This is using pygame, that uses SDL under the hood.
# An alternative implementation could be using GLFW.
class PygameCursor(BaseCursor):
    def set_mouse_cursor(self, new_cursor: str) -> None:
        cursors: Dict[str, Any] = {
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
