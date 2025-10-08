from typing import Any, Tuple

import pygame

from client.engine.backend.foundational_wrapper import (
    FoundationalColor,
    FoundationalSurface,
)
from client.engine.backend.graphics.graphics import GraphicsBackend
from client.engine.primitives.shape import Shape

from .sprite import Sprite

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)

from OpenGL.GL import (
    GL_LINEAR,
    GL_QUADS,
    GL_RGBA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_UNPACK_ALIGNMENT,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glDisable,
    glEnable,
    glEnd,
    glGenTextures,
    glPixelStorei,
    glPopMatrix,
    glPushMatrix,
    glTexCoord2f,
    glTexImage2D,
    glTexParameteri,
    glTranslatef,
    glVertex2f,
)


# This all depends on PYGAME/OPENGL
class Text(Shape):
    def __init__(self, message: str, x: int, y: int, color: FoundationalColor = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:
            font = GraphicsBackend.get().get_font(
                GraphicsBackend.get().get_default_font(), 24
            )
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message: str) -> None:
        self.message = message


class Rectangle(Shape):
    def __init__(
        self, x: int, y: int, width: int, height: int, color: FoundationalColor = BLACK
    ):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:
            rectangle = FoundationalSurface((self.width, self.height))
            rectangle.fill(self.color)
            rectangle.set_alpha(128)  # TODO: Alpha could be passed
            window.blit(rectangle, dest=(self.x, self.y))


class SmallText(Shape):
    def __init__(self, message: str, x: int, y: int, color: FoundationalColor = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window: Any) -> None:
        if window is not None:
            font = GraphicsBackend.get().get_font(
                GraphicsBackend.get().get_default_font(), 12
            )
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message: str) -> None:
        self.message = message


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
        self.image = GraphicsBackend().get().load_image(path)

    def render(self, window: Any) -> None:
        if not hasattr(self, "texture_id"):
            self.texture_id = self._create_opengl_texture(self.image)
        # This is ONLY for OpenGL
        if window is not None:
            # This is ONLY for Pygame Native
            # window.blit(self.image, dest=(self.x, self.y))
            # This is only for OpenGL
            glPushMatrix()

            # Step 2: Bind the texture and draw a quad
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            # Apply the image's position to the current matrix
            glTranslatef(self.x, self.y, 0)

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


class Animation(Shape):
    def __init__(self, folder: str, x: int, y: int, initial_frame: int = 0):
        super().__init__(x, y)
        self.sprite_group = GraphicsBackend.get().sprite_group()
        self.animation = Sprite(folder, x, y, initial_frame)
        self.sprite_group.add(self.animation)

    def set_x(self, x: int) -> None:
        super().set_x(x)
        self.animation.set_x(x)

    def set_y(self, y: int) -> None:
        super().set_y(y)
        self.animation.set_y(y)

    def update(self) -> None:
        self.sprite_group.update()  # Calls update on every sprite on the group

    def render(self, window: Any) -> None:
        if window is not None:
            self.sprite_group.draw(window)

    def get_x(self) -> int:
        return self.animation.get_x()

    def get_y(self) -> int:
        return self.animation.get_y()

    def get_width(self) -> int:
        return self.animation.get_width()

    def get_height(self) -> int:
        return self.animation.get_width()
