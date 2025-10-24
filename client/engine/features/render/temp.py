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
        return None

    def render(self, window) -> None:
        for shape in self.shapes:
            shape.draw(
                self.state.get_x(), self.state.get_y(), window, self.state.get_index()
            )
        return None

    def _is_point_in_shape(self, x, y, shape):
        return (
            x > shape.get_x()
            and x < shape.get_x() + shape.get_width()
            and y > shape.get_y()
            and y < shape.get_y() + shape.get_height()
        )

    def contains_point(self, x, y):
        for shape in self.shapes:
            if self._is_point_in_shape(x, y, shape):
                return True

        return False


# A screen render is a collection of UI Elements that will be
# drawn in the screen
class ScreenRender(ABC):
    def __init__(self, render_elements) -> None:
        self.render_elements = render_elements

    def render(self, window) -> None:
        for render_element in self.render_elements:
            render_element.render(window)

    def load(self) -> None:
        for render_element in self.render_elements:
            render_element.load()


def create_render_from_screen(screen):
    return ScreenRender([ui_element.get_render() for ui_element in screen.ui_elements])
