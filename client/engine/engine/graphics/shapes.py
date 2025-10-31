from engine.backend.constants import GRAPHICS
from engine.backend.graphics.native.shapes.animation import Animation as AnimationNative
from engine.backend.graphics.native.shapes.image import Image as ImageNative
from engine.backend.graphics.native.shapes.rectangle import Rectangle as RectangleNative
from engine.backend.graphics.native.shapes.text import Text as TextNative
from engine.backend.graphics.opengl.shapes.animation import Animation as AnimationOpengl
from engine.backend.graphics.opengl.shapes.image import Image as ImageOpengl
from engine.backend.graphics.opengl.shapes.rectangle import Rectangle as RectangleOpengl
from engine.backend.graphics.opengl.shapes.text import Text as TextOpengl

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
