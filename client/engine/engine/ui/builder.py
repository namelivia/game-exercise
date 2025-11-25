import os

from engine.animation.loader import load_animation
from engine.features.render.ui_element import UIElementRender
from engine.graphics.shapes import Animation, Image, Rectangle, Text

from .logic import UIElementLogic
from .state import UIElementState
from .ui import UIElement


class UIBuilder:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self._shapes = []
        self._logic_class = None

    def with_image(self, path: str, x=0, y=0, visible=True, name=None):
        image = Image(path, x, y)
        if not visible:
            image.hide()
        if name:
            image.set_name(name)
        self._shapes.append(image)
        return self

    def with_text(self, message: str, x=0, y=0, visible=True, name=None):
        text = Text(message, x, y)
        if not visible:
            text.hide()
        if name:
            text.set_name(name)
        self._shapes.append(text)
        return self

    def with_rectangle(self, x=0, y=0, width=0, height=0, visible=True, name=None):
        rectangle = Rectangle(x, y, width, height)
        if not visible:
            rectangle.hide()
        if name:
            rectangle.set_name(name)
        self._shapes.append(rectangle)
        return self

    def with_animation(self, json_file_path: str, x=0, y=0, fps: int = 10):
        sprite_data = load_animation(json_file_path)
        json_file_dir = os.path.abspath(os.path.dirname(json_file_path))
        animation_shape = Animation(
            os.path.join(json_file_dir, sprite_data.image),
            x,
            y,
            sprite_data.rows,
            sprite_data.columns,
            sprite_data.animations,
            fps,
        )
        self._shapes.append(animation_shape)
        return self

    def with_logic(self, logic):
        self._logic_class = logic
        return self

    def build(self):
        state = UIElementState(self.x, self.y)
        render = UIElementRender(state, self._shapes)
        logic_instance = None
        if self._logic_class:
            logic_instance = self._logic_class(state, render)
        else:
            logic_instance = UIElementLogic(state, render)
        return UIElement(render, logic_instance)
