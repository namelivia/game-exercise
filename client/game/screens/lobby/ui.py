from client.graphics.shapes import Text
from client.primitives.ui import UIElement


class WelcomeMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text(f'Welcome to game, {name}', 20, 0)
        ]


class OptionList(UIElement):
    def __init__(self, options):
        self.options = options
        self.shapes = []
        for index, option in self.options.items():
            self.shapes.append(
                Text(f'{index} - {option}', 20, 200 + (30 * int(index)))
            )