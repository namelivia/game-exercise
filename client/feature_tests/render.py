from client.engine.features.render.worker import RenderWorker
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.graphics.shapes import Image
from client.engine.primitives.screen import Screen
from client.engine.primitives.ui import UIElement


class Background(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.set_shapes([Image("client/experiment/images/background.png", 0, 0)])


class TestScreen(Screen):
    def __init__(self) -> None:
        self.ui_elements = [
            Background(),
        ]


if __name__ == "__main__":
    screen = CurrentScreen()
    screen.initialize()
    screen.set_current_screen(TestScreen())
    render_thread = RenderWorker(name="Render")
    render_thread.start()
