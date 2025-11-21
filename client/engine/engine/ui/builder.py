from engine.graphics.shapes import Image, Text

from .factory import create_ui_element
from .state import UIElementState


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

    def with_logic(self, logic):
        self._logic_class = logic
        return self

    def build(self):
        state = UIElementState(self.x, self.y)
        logic_instance = None
        if self._logic_class:
            logic_instance = self._logic_class(state)
        return create_ui_element(
            shapes=self._shapes,
            state=state,
            custom_logic=logic_instance,
        )
