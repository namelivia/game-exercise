from abc import ABC


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
