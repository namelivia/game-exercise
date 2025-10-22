from client.engine.backend.constants import GRAPHICS
from client.engine.backend.graphics.native.shapes.animation import (
    Animation as AnimationNative,
)
from client.engine.backend.graphics.native.shapes.image import Image as ImageNative
from client.engine.backend.graphics.native.shapes.rectangle import (
    Rectangle as RectangleNative,
)
from client.engine.backend.graphics.native.shapes.text import Text as TextNative
from client.engine.backend.graphics.opengl.shapes.animation import (
    Animation as AnimationOpengl,
)
from client.engine.backend.graphics.opengl.shapes.image import Image as ImageOpengl
from client.engine.backend.graphics.opengl.shapes.rectangle import (
    Rectangle as RectangleOpengl,
)
from client.engine.backend.graphics.opengl.shapes.text import Text as TextOpengl

if GRAPHICS == "NATIVE":
    Text = TextNative
    Rectangle = RectangleNative
    Image = ImageNative
    Animation = AnimationNative
else:
    Text = TextOpengl
    Rectangle = RectangleOpengl
    Image = ImageOpengl
    Animation = AnimationOpengl
