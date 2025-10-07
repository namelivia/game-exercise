from typing import TYPE_CHECKING

from client.engine.backend.graphics import PygameNativeGraphicsBackend

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


class Graphics:
    def __init__(self) -> None:
        self.window = PygameNativeGraphicsBackend.get_new_window(640, 480)

    # THIS DEPENDS ON PYGAME/OPENGL
    def render(self, screen: "Screen") -> None:
        ui_elements = screen.get_ui_elements()
        self.window.fill((255, 255, 255))
        for ui_element in ui_elements:
            ui_element.render(self.window)
        PygameNativeGraphicsBackend.update_display()
        return None
