from client.engine.backend.constants import GRAPHICS
from client.engine.backend.graphics.native.shapes import Animation as AnimationNative
from client.engine.backend.graphics.native.shapes import Image as ImageNative
from client.engine.backend.graphics.native.shapes import Rectangle as RectangleNative
from client.engine.backend.graphics.native.shapes import SmallText as SmallTextNative
from client.engine.backend.graphics.native.shapes import Text as TextNative
from client.engine.backend.graphics.opengl.shapes import Animation as AnimationOpengl
from client.engine.backend.graphics.opengl.shapes import Image as ImageOpengl
from client.engine.backend.graphics.opengl.shapes import Rectangle as RectangleOpengl
from client.engine.backend.graphics.opengl.shapes import SmallText as SmallTextOpengl
from client.engine.backend.graphics.opengl.shapes import Text as TextOpengl

if GRAPHICS == "NATIVE":
    Text = TextNative
    Rectangle = RectangleNative
    SmallText = SmallTextNative
    Image = ImageNative
    Animation = AnimationNative
else:
    Text = TextOpengl
    Rectangle = RectangleOpengl
    SmallText = SmallTextOpengl
    Image = ImageOpengl
    Animation = AnimationOpengl
