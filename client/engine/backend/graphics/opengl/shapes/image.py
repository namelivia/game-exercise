from typing import Any

from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)

from OpenGL.GL import (
    GL_LINEAR,
    GL_QUADS,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glDisable,
    glEnable,
    glEnd,
    glGenTextures,
    glPopMatrix,
    glPushMatrix,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glTranslatef,
    glVertex2f,
)


class Image(Shape):
    def _create_opengl_texture(self, image):
        img_data = image.convert("RGBA").tobytes()
        width = image.width
        height = image.height

        # 3. Generate and bind texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # 4. Upload data directly from Pillow
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data,
        )
        return texture_id

    def __init__(self, path: str, x: int, y: int):
        super().__init__(x, y)
        self.path = path

    def load(self):
        self.image = GraphicsBackend().get().load_image(self.path)
        self.texture_id = self._create_opengl_texture(self.image)

    def render(self, x, y, window: Any) -> None:
        if window is not None:
            dest_x = self.x + x
            dest_y = self.y + y
            glPushMatrix()

            # Step 2: Bind the texture and draw a quad
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            # Apply the image's position to the current matrix
            glTranslatef(dest_x, dest_y, 0)

            # Draw a quad using texture coordinates (0,0 to 1,1)
            glBegin(GL_QUADS)
            # Top-Left Vertex
            glTexCoord2f(0, 1)  # T(U, V=1) - Map to TOP of the texture
            glVertex2f(0, 0)

            # Top-Right Vertex
            glTexCoord2f(1, 1)  # T(U=1, V=1)
            glVertex2f(self.get_width(), 0)

            # Bottom-Right Vertex
            glTexCoord2f(1, 0)  # T(U=1, V=0) - Map to BOTTOM of the texture
            glVertex2f(self.get_width(), self.get_height())

            # Bottom-Left Vertex
            glTexCoord2f(0, 0)  # T(U, V=0)
            glVertex2f(0, self.get_height())
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)  # Unbind
            glDisable(GL_TEXTURE_2D)

            glPopMatrix()

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_width(self) -> int:
        return self.image.width

    def get_height(self) -> int:
        return self.image.height
