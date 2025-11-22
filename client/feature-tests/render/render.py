from engine.clock import Clock
from engine.features.render.commands import StartRendering
from engine.features.render.worker import RenderWorker
from engine.primitives.screen import Screen
from engine.queue import QueueManager
from engine.ui.builder import UIBuilder


class TestScreen(Screen):
    def __init__(self) -> None:
        self.ui_elements = [
            (
                UIBuilder(x=0, y=0)
                .with_image("images/background.png")
                .with_text("This is a test", 20, 20)
                .with_rectangle(0, 0, 20, 20)
                .build()
            ),
            (
                UIBuilder(x=150, y=150)
                .with_animation("images/animation_debug.json", 0, 0, 2)
                .with_animation("images/animation_debug.json", 100, 100, 6)
                .build()
            ),
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
