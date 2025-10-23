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
            shape.draw(self.state.get_x(), self.state.get_y(), window)
        return None

    def contains_point(self, x, y):
        return (
            x > self.shapes[0].get_x()
            and x < self.shapes[0].get_x() + self.shapes[0].get_width()
            and y > self.shapes[0].get_y()
            and y < self.shapes[0].get_y() + self.shapes[0].get_height()
        )


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
