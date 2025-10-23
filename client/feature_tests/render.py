from client.engine.clock import Clock
from client.engine.features.render.commands import StartRendering
from client.engine.features.render.worker import RenderWorker
from client.engine.general_state.queue import QueueManager
from client.engine.graphics.shapes import Animation, Image, Rectangle, Text
from client.engine.primitives.screen import Screen
from client.engine.primitives.ui import create_ui_element


class TestScreen(Screen):
    def __init__(self) -> None:
        self.ui_elements = [
            create_ui_element(
                [
                    Image("client/experiment/images/background.png", 0, 0),
                    Text(f"This is a test", 20, 20),
                    Rectangle(0, 0, 20, 20),
                    Animation("client/game/images/coin", 250, 0, 3),
                ]
            )
        ]


if __name__ == "__main__":
    QueueManager().initialize()
    Clock().initialize()
    render_thread = RenderWorker(
        name="Render",
        queue=QueueManager().get("render"),
    )
    render_thread.start()
    StartRendering(TestScreen()).execute()
