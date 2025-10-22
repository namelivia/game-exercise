from typing import Any

from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)

from OpenGL.GL import (
    GL_QUADS,
    glBegin,
    glColor3f,
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

    def render(self, window: Any) -> None:
        # Start a new matrix scope
        glPushMatrix()

        glColor3f(self.color[0], self.color[1], self.color[2])

        # Apply the rectangle's top-left position (x, y)
        glTranslatef(self.x, self.y, 0)

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
        glColor3f(1.0, 1.0, 1.0)
