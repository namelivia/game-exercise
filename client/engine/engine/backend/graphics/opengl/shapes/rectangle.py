from typing import Any

from engine.backend.foundational_wrapper import FoundationalColor
from engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)

from OpenGL.GL import (
    GL_BLEND,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_QUADS,
    GL_SRC_ALPHA,
    glBegin,
    glBlendFunc,
    glColor4f,
    glDisable,
    glEnable,
    glEnd,
    glPopMatrix,
    glPushMatrix,
    glTranslatef,
    glVertex2f,
)


class Rectangle(Shape):
    def __init__(
        self, x: int, y: int, width: int, height: int, color: FoundationalColor = BLACK
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def render(self, x, y, opacity, window: Any, index) -> None:
        dest_x = self.x + x
        dest_y = self.y + y
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Start a new matrix scope
        glPushMatrix()

        glColor4f(self.color[0], self.color[1], self.color[2], opacity)

        # Apply the rectangle's top-left position (x, y)
        glTranslatef(dest_x, dest_y, 0)

        # Draw a filled quad for the rectangle
        glBegin(GL_QUADS)

        # Vertex 1: Top-Left (relative to the translated origin)
        glVertex2f(0, 0)

        # Vertex 2: Top-Right
        glVertex2f(self.width, 0)

        # Vertex 3: Bottom-Right
        glVertex2f(self.width, self.height)

        # Vertex 4: Bottom-Left
        glVertex2f(0, self.height)

        glEnd()

        # Restore the previous matrix
        glPopMatrix()

        # Reset color
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glDisable(GL_BLEND)

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height
