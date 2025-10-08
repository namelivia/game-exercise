from ..constants import GRAPHICS
from .native.native import PygameNativeGraphicsBackend
from .opengl.opengl import PygameOpenGLGraphicsBackend


class GraphicsBackend:

    @staticmethod
    def get():
        if GRAPHICS == "NATIVE":
            return PygameNativeGraphicsBackend()
        else:
            return PygameOpenGLGraphicsBackend()
