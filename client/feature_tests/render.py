from client.engine.features.render.commands import StartRendering
from client.engine.features.render.state import State
from client.engine.features.render.worker import RenderWorker
from client.engine.general_state.queue import QueueManager
from client.engine.graphics.shapes import Image, Text
from client.engine.primitives.screen import Screen
from client.engine.primitives.ui import UIElement


class Background(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.set_shapes(
            [
                Image("client/experiment/images/background.png", 0, 0),
                Text(f"This is a test", 20, 20),
            ]
        )


class TestScreen(Screen):
    def __init__(self) -> None:
        self.ui_elements = [
            Background(),
        ]


if __name__ == "__main__":
    QueueManager().initialize()
    render_thread = RenderWorker(
        name="Render",
        queue=QueueManager().get("render"),
    )
    render_thread.start()
    StartRendering(TestScreen().get_render()).execute()
