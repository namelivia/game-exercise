from client.graphics.shapes import Text
from client.primitives.ui import UIElement


# UI components than can be shared among many screens
class ClockUI(UIElement):
    def __init__(self, value):
        self.shapes = [
            Text(f'Time is {value}', 20, 100)
        ]

    def update(self, time, data):
        self.shapes[0].set_message(f'Time is {time}')  # Not supersure about this
