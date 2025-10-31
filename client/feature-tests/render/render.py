from engine.animation_factory import create_animation
from engine.clock import Clock
from engine.features.render.commands import StartRendering
from engine.features.render.worker import RenderWorker
from engine.graphics.shapes import Image, Rectangle, Text
from engine.primitives.screen import Screen
from engine.primitives.ui import create_ui_element
from engine.queue import QueueManager


class TestScreen(Screen):
    def __init__(self) -> None:
        self.ui_elements = [
            create_ui_element(
                [
                    Image("images/background.png", 0, 0),
                    Text(f"This is a test", 20, 20),
                    Rectangle(0, 0, 20, 20),
                ]
            ),
            create_animation("images/animation_debug.json", 50, 50, 2),
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
