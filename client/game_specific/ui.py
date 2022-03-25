from abc import ABC
from client.graphics.shapes import Text

# Each of these are ANIMATIONS (thats why they have time)


class UIElement(ABC):

    # No animations yet
    # def render(self, time, window):
    def render(self, window):
        [shape.render(window) for shape in self.shapes]


class WelcomeMessage(UIElement):
    def __init__(self):
        self.shapes = [
            Text('Welcome to Game', 20, 0)
        ]


class OptionList(UIElement):
    def __init__(self, options):
        self.options = options
        self.shapes = []
        for index, option in self.options.items():
            self.shapes.append(
                Text(f'{index} - {option}', 20, 200 + (30 * int(index)))
            )


class ClockUI(UIElement):
    def __init__(self, clock):
        self.clock = clock
        self.shapes = [
            Text('Time is (update pending)', 20, 100)
        ]


class NewGameMessage(UIElement):
    def __init__(self):
        self.shapes = [
            Text('Create a new game', 20, 0),
            Text('Please write the name for your new game:', 20, 40)
        ]
