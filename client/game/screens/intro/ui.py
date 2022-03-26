from client.graphics.shapes import Text
from client.primitives.ui import UIElement


class Title(UIElement):
    def __init__(self, value):
        self.shapes = [
            Text('Welcome to the game', 20, 10)
        ]

    def update(self, time, data):
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.shapes[0].set_x((time/inverse_speed) % (640 + offset) - offset)  # Not supersure about this
