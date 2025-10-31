from typing import Any, Dict

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

from ..base import BaseGraphicsBackend


class PygameOpenGLGraphicsBackend(BaseGraphicsBackend):
    def update_display(self) -> None:
        pygame.display.flip()
        return None

    def load_image(self, path: str):
        return Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)

    def _setup_opengl_view(self, width, height):
        # This sets up the view in OpenGL for a 2D application
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def get_new_window(self, width: int, height: int) -> pygame.Surface:
        window = pygame.display.set_mode(
            (width, height), pygame.OPENGL | pygame.DOUBLEBUF
        )
        self._setup_opengl_view(width, height)
        return window

    def clear_window(self, window):
        glClear(GL_COLOR_BUFFER_BIT)
