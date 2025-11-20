from engine.graphics.shapes import Image

from .factory import create_ui_element
from .state import UIElementState


class UIBuilder:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self._shapes = []
        self._logic = None

    def with_image(self, path: str, x=0, y=0, visible=True, name=None):
        image = Image(path, x, y)
        if not visible:
            image.hide()
        if name:
            image.set_name(name)
        self._shapes.append(image)
        return self

    def with_logic(self, logic):
        self._logic = logic
        return self

    def build(self):
        return create_ui_element(
            shapes=self._shapes,
            state=UIElementState(self.x, self.y),
            custom_logic=self._logic,
        )
