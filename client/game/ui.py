from client.engine.graphics.shapes import Text, Animation
from client.engine.primitives.ui import UIElement


# UI components than can be shared among many screens
class ClockUI(UIElement):
    def __init__(self, value):
        self.shapes = [Text(f"Time is {value}", 20, 100)]

    def update(self, time, data):
        self.shapes[0].set_message(f"Time is {time}")  # Not supersure about this


class AnimationDebug(UIElement):
    def __init__(self):
        self.shapes = [
            Animation("client/game/images/debug", 250, 0, 3),
        ]

    def update(self, time, data):
        self.shapes[0].update()
