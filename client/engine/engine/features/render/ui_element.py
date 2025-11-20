from abc import ABC


# A UI Element render is a collection of shapes that will be
# drawn in the screen
class UIElementRender(ABC):
    def __init__(self, state, shapes) -> None:
        self.state = state
        self.shapes = shapes

    def show(self) -> None:
        for shape in self.shapes:
            shape.show()

    def hide(self) -> None:
        for shape in self.shapes:
            shape.hide()

    def load(self) -> None:
        for shape in self.shapes:
            shape.load()

    def find_shape(self, name: str):
        for shape in self.shapes:
            if getattr(shape, "name", None) == name:
                return shape
        return None

    def render(self, window) -> None:
        for shape in self.shapes:
            shape.draw(
                self.state.get_x(), self.state.get_y(), window, self.state.get_index()
            )

    def _is_point_in_shape(self, x: int, y: int, shape) -> bool:
        return (
            x > shape.get_x()
            and x < shape.get_x() + shape.get_width()
            and y > shape.get_y()
            and y < shape.get_y() + shape.get_height()
        )

    def contains_point(self, x: int, y: int) -> bool:
        for shape in self.shapes:
            if self._is_point_in_shape(x, y, shape):
                return True
        return False
