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


class Animation(Shape):
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

    def __init__(self, path: str, x: int, y: int, rows: int, cols: int):
        super().__init__(x, y)
        self.path = path
        self.rows = rows
        self.cols = cols
        self.animation_frames = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.current_frame = self.animation_frames[0]

    def load(self):
        self.image = GraphicsBackend().get().load_image(self.path)
        self.texture_id = self._create_opengl_texture(self.image)

    def _get_frame_uvs(self, index):
        # 1. Determine the frame's position in the grid
        row = index // self.cols
        col = index % self.cols

        # 2. Calculate pixel coordinates (x, y, x_end, y_end)
        x_start_px = col * self.get_width()
        y_start_px = row * self.get_height()
        x_end_px = x_start_px + self.get_width()
        y_end_px = y_start_px + self.get_height()

        # 3. Normalize coordinates (convert to UVs 0.0 to 1.0)
        # U (horizontal) is based on total width
        u_min = x_start_px / self.image.width
        u_max = x_end_px / self.image.width

        # V (vertical) is based on total height (Note: OpenGL's V=0 is often the bottom of the image)
        # The image data is usually loaded with V=0 being the bottom.
        v_min = y_start_px / self.image.height
        v_max = y_end_px / self.image.height

        # To ensure consistency with the original code's V mapping:
        # Original code: V=0 is BOTTOM (y=height), V=1 is TOP (y=0)
        # So we need to flip the calculated V values based on the pixel space:
        v_bottom = 1.0 - (
            y_end_px / self.image.height
        )  # Maps y_end_px (bottom of frame) to the texture's V-bottom (0.0)
        v_top = 1.0 - (
            y_start_px / self.image.height
        )  # Maps y_start_px (top of frame) to the texture's V-top (1.0)

        # Return (u_min, v_bottom, u_max, v_top)
        return u_min, v_bottom, u_max, v_top

    def render(self, x, y, window: Any) -> None:
        if window is not None:

            u_min, v_bottom, u_max, v_top = self._get_frame_uvs(self.current_frame)

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
            glTexCoord2f(u_min, v_top)
            glVertex2f(0, 0)

            # Top-Right Vertex
            glTexCoord2f(u_max, v_top)
            glVertex2f(self.get_width(), 0)

            # Bottom-Right Vertex
            glTexCoord2f(u_max, v_bottom)
            glVertex2f(self.get_width(), self.get_height())

            # Bottom-Left Vertex
            glTexCoord2f(u_min, v_bottom)
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
        return self.image.width // self.cols

    def get_height(self) -> int:
        return self.image.height // self.rows
