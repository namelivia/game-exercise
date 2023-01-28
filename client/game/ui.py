from client.engine.graphics.shapes import Text, Animation
from typing import Dict, Any
from client.engine.primitives.ui import UIElement


# UI components than can be shared among many screens
class ClockUI(UIElement):
    def __init__(self, value: int):
        self.shapes = [Text(f"Time is {value}", 20, 100)]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.shapes[0].set_message(f"Time is {time}")  # Not supersure about this


class AnimationDebug(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Animation("client/game/images/debug", 250, 0, 3),
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.shapes[0].update()
