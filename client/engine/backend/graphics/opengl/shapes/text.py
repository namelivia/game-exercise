from typing import Any

from client.engine.backend.foundational_wrapper import FoundationalColor
from client.engine.primitives.shape import Shape

WHITE = FoundationalColor(255, 255, 255)
BLACK = FoundationalColor(0, 0, 0)

import freetype
import numpy as np
from OpenGL.GL import (
    GL_ALPHA,
    GL_BLEND,
    GL_CLAMP_TO_EDGE,
    GL_LINEAR,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_QUADS,
    GL_RGBA,
    GL_SRC_ALPHA,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_UNPACK_ALIGNMENT,
    GL_UNSIGNED_BYTE,
    glBegin,
    glBindTexture,
    glBlendFunc,
    glColor3f,
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


# This stores info for each character in the font
class CharacterSlot:
    def __init__(self, texture_id, size, bearing, advance):
        self.texture_id = texture_id  # The OpenGL texture ID (or UV coords later)
        self.size = size  # Glyph width and height (w, h)
        self.bearing = bearing  # Offset from baseline to top-left of glyph (x, y)
        self.advance = advance  # Horizontal offset to advance to the next glyph (x)


# This all depends on PYGAME/OPENGL
class Text(Shape):
    def __init__(self, message: str, x: int, y: int, color: FoundationalColor = BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def _store_gliph_information(self, face):
        Characters = {}

        # Disable byte-alignment restriction, which is common for monochrome (GL_RED) textures
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Loop through the ASCII characters you want to support (32 to 127)
        for char_code in range(32, 128):
            char = chr(char_code)

            # 1. Load the glyph
            # FT_LOAD_RENDER tells FreeType to rasterize the glyph into a bitmap
            # face.load_char(char, freetype.FT_LOAD_RENDER)
            face.load_char(
                char
            )  # In freetype-py, rendering happens by default with load_char

            glyph = face.glyph

            # 2. Generate the Texture (for this single character)
            # The bitmap data from FreeType is stored in face.glyph.bitmap
            bitmap = glyph.bitmap

            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)

            # Create the texture from the glyph bitmap buffer
            # Note: FreeType glyphs are typically 8-bit grayscale (GL_RED)
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_ALPHA,  # Internal format: typically GL_RED for grayscale alpha
                bitmap.width,
                bitmap.rows,
                0,
                GL_ALPHA,  # Format of the pixel data
                GL_UNSIGNED_BYTE,
                # Convert the buffer to a numpy array for direct use
                np.array(bitmap.buffer, dtype=np.ubyte),
            )

            # 3. Set texture parameters (crucial for clean text rendering)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR
            )  # Linear filtering for smooth text
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # 4. Store the metrics
            Characters[char] = CharacterSlot(
                texture,
                (glyph.bitmap.width, glyph.bitmap.rows),
                (glyph.bitmap_left, glyph.bitmap_top),
                # Advance is usually stored in 1/64th of a pixel, so shift right by 6 (>> 6)
                glyph.advance.x >> 6,
            )

        # Bind back to the default texture
        glBindTexture(GL_TEXTURE_2D, 0)
        return Characters

    def load(self):
        font_path = "client/experiment/fonts/AccidentalPresidency.ttf"
        size = 24

        # Load font file
        self.face = freetype.Face(font_path)
        self.face.set_pixel_sizes(0, size)
        self.font_ascent = self.face.ascender >> 6

        # TODO: This should happen once per font, not per string
        self.Characters = self._store_gliph_information(self.face)

    def _render_character(self, x, y, char, Characters, face):
        scale = 1.0  # Hardcode this for now
        if char not in Characters:
            # Optionally, render a placeholder or skip
            x += (
                face.glyph.advance.x >> 6
            ) * scale  # Use a generic advance if possible
            return x

        ch = Characters[char]

        # Calculate character position (w, h is glyph size, bearing is offset)
        w = ch.size[0] * scale
        h = ch.size[1] * scale

        # x_offset: Horizontal offset from the cursor position to the bitmap's left edge
        x_offset = x + ch.bearing[0] * scale

        # The rendering quad's corner positions:
        x_left = x_offset
        y_top = y - ch.bearing[1] * scale

        # Use glPushMatrix/glPopMatrix for matrix isolation and translation
        glPushMatrix()

        # Translate the drawing origin to the calculated top-left corner of the quad
        # The vertices below will be relative to this new origin.
        glTranslatef(x_left, y_top, 0)

        # Bind the specific texture for this character
        glBindTexture(GL_TEXTURE_2D, ch.texture_id)

        # Draw the character quad
        glBegin(GL_QUADS)

        # Your image code's coordinate system (0,0 is Top-Left of quad):
        # Top-Left Vertex: (0, 0) in local space
        glTexCoord2f(0, 0)  # U=0, V=0
        glVertex2f(0, 0)

        # Top-Right Vertex: (w, 0)
        glTexCoord2f(1, 0)  # U=1, V=0
        glVertex2f(w, 0)

        # Bottom-Right Vertex: (w, h)
        glTexCoord2f(1, 1)  # U=1, V=1
        glVertex2f(w, h)

        # Bottom-Left Vertex: (0, h)
        glTexCoord2f(0, 1)  # U=0, V=1
        glVertex2f(0, h)

        glEnd()

        # Clean up this character's state
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

        # Advance the cursor for the next character
        return x + ch.advance * scale

    def render(self, x, y, window: Any, index) -> None:
        dest_x = self.x + x
        dest_y = self.y + y
        scale = 1.0  # Hardcoding this value for now
        x = dest_x  # Current horizontal position (cursor)
        y = dest_y + self.font_ascent * scale

        # 1. Enable Blending for transparency (essential for anti-aliasing)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 2. Enable Texturing and set the color
        glEnable(GL_TEXTURE_2D)
        glColor3f(self.color[0], self.color[1], self.color[2])

        for char in self.message:
            x = self._render_character(x, y, char, self.Characters, self.face)

        # Final cleanup
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glColor3f(1.0, 1.0, 1.0)  # Reset color

    def set_message(self, message: str) -> None:
        self.message = message
