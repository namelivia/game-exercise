from .native import PygameNativeGraphicsBackend
from .opengl import PygameOpenGLGraphicsBackend


class GraphicsBackend:

    TYPE = "OPENGL"

    @staticmethod
    def get():
        if GraphicsBackend.TYPE == "NATIVE":
            return PygameNativeGraphicsBackend()
        else:
            return PygameOpenGLGraphicsBackend()
