from typing import Any, Dict

from engine.api import MousePosition, UIBuilder, UIElementLogic


class ImageCursorLogic(UIElementLogic):

    def update(self, time: int, data: Dict[str, Any]) -> None:
        super().update(time, data)
        mouse_position = MousePosition().get()
        self.state.set_x(mouse_position[0])
        self.state.set_y(mouse_position[1])


class ImageCursor:
    def __init__(self):
        self.element = None

    def initialize(self, cursors):
        element = UIBuilder(x=0, y=0).with_logic(ImageCursorLogic)
        for cursor, path in cursors.items():
            element = element.with_image(path, -12, -11, False, cursor)
        self.element = element.build()

    def get_element(self):
        return self.element

    def set_cursor(self, key):
        if self.element is not None:
            self.element.hide()
            self.element.get_render().find_shape(key).show()
