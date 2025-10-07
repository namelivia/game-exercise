from abc import ABC, abstractmethod
from typing import Any, Dict

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class BaseGraphicsBackend(ABC):

    @abstractmethod
    def update_display(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_new_window(self, width: int, height: int) -> pygame.Surface:
        raise NotImplementedError

    @abstractmethod
    def set_mouse_cursor(self, new_cursor: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def sprite_group(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_default_font(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_font(self, font: str, size: int) -> pygame.font.Font:
        raise NotImplementedError


class PygameGraphicsBackend(BaseGraphicsBackend):
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

    def get_default_font(self) -> str:
        return pygame.font.get_default_font()

    def get_font(self, font: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font, size)

    def sprite_group(self) -> Any:
        return pygame.sprite.Group()


class PygameNativeGraphicsBackend(PygameGraphicsBackend):
    def update_display(self) -> None:
        pygame.display.update()
        return None

    def get_new_window(self, width: int, height: int) -> pygame.Surface:
        return pygame.display.set_mode((width, height), pygame.DOUBLEBUF)


class PygameOpenGLGraphicsBackend(PygameGraphicsBackend):
    def update_display(self) -> None:
        pygame.display.flip()
        return None

    def get_new_window(self, width: int, height: int) -> pygame.Surface:
        window = pygame.display.set_mode(
            (width, height), pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF
        )
        # 2. Set the Viewport (which part of the window to render to)
        glViewport(0, 0, width, height)

        # 3. Set up the PROJECTION matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Set up a 2D projection (e.g., matching screen pixels)
        # This is crucial for fixing the blurriness you were seeing!
        gluOrtho2D(0, width, height, 0)  # Left, Right, Bottom, Top (Flipped Y)

        # 4. Set the MODELVIEW matrix (where objects are placed/rotated)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        return window


class GraphicsBackend:

    TYPE = "OPENGL"

    @staticmethod
    def get():
        if GraphicsBackend.TYPE == "NATIVE":
            return PygameNativeGraphicsBackend()
        else:
            return PygameOpenGLGraphicsBackend()
