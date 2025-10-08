from typing import Any, Dict

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

from .pygame_window import PygameGraphicsBackend


class PygameOpenGLGraphicsBackend(PygameGraphicsBackend):
    def update_display(self) -> None:
        pygame.display.flip()
        return None

    def load_image(self, path: str):
        return Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)

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
