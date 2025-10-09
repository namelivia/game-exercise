import freetype
import numpy as np
from OpenGL.GL import *


def load_glyph_texture(face, char_code):
    """
    Loads a single FreeType glyph, converts its 8-bit grayscale bitmap
    to a GL_R8 (Red) texture, and returns the texture ID and glyph metrics.

    Args:
        face (freetype.Face): The loaded FreeType font face object.
        char_code (str): The single character to load (e.g., 'A').

    Returns:
        tuple: (texture_id, metrics_dict) or (None, None) on error.
    """
    try:
        # 1. Load the glyph (FT_LOAD_RENDER ensures an 8-bit grayscale bitmap)
        face.load_char(char_code, freetype.FT_LOAD_RENDER)
        glyph = face.glyph
        bitmap = glyph.bitmap

        # FreeType-py buffer is a ctypes array, convert it to a NumPy array for GL upload
        buffer_data = np.frombuffer(bitmap.buffer, dtype=np.ubyte)

        width = bitmap.width
        rows = bitmap.rows

        # --- OpenGL Texture Generation ---

        # 2. Generate and Bind the Texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # 3. Set Texture Parameters
        # Linear filtering for smooth anti-aliased look
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # 4. Set UNPACK_ALIGNMENT
        # FreeType bitmaps are tightly packed (1 byte alignment), we must tell OpenGL this.
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # 5. Upload the Texture Data
        # Internal Format: GL_R8 (1-channel, 8-bit Red)
        # Input Format: GL_RED (Our data is single-channel, we'll read it in the shader)
        # Input Type: GL_UNSIGNED_BYTE (8-bit data)

        glTexImage2D(
            GL_TEXTURE_2D,  # target
            0,  # level
            GL_R8,  # internalformat (Single-channel, 8-bit R)
            width,  # width
            rows,  # height
            0,  # border
            GL_RED,  # format (Source data is Red channel data)
            GL_UNSIGNED_BYTE,  # type (Source data is 8-bit bytes)
            buffer_data,  # data
        )

        # 6. Collect Metrics (same as your original example, converted to float/int)
        metrics = {
            "width": width,
            "height": rows,
            # Horizontal position relative to the cursor
            "x_offset": glyph.bitmap_left,
            # Vertical position relative to the baseline (positive is up)
            "y_offset": glyph.bitmap_top,
            # Move to the start of the next character (in 1/64ths, converted to pixels)
            "advance_x": glyph.advance.x // 64,
        }

        # Unbind the texture
        glBindTexture(GL_TEXTURE_2D, 0)

        return texture_id, metrics

    except Exception as e:
        print(f"Error loading glyph for character: {char_code}. Error: {e}")
        return None, None
