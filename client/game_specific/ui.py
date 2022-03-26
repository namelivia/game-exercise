from abc import ABC
from client.graphics.shapes import Text

# Each of these are ANIMATIONS (thats why they have time)


class UIElement(ABC):

    # No animations yet
    # def render(self, time, window):
    # UI elements can hold a small state too that can be updated
    def render(self, window):
        [shape.render(window) for shape in self.shapes]

    def update(self, data):
        pass


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


class ClockUI(UIElement):
    def __init__(self, value):
        self.shapes = [
            Text(f'Time is {value}', 20, 100)
        ]

    def update(self, data):
        # What if data does not contain time? Throw an exception
        time = data['time']
        self.shapes[0].set_message(f'Time is {time}')  # Not supersure about this


class NewGameMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text('Create a new game', 20, 0),
            Text('Please write the name for your new game:', 20, 40),
            Text(name, 20, 70)
        ]

    def update(self, data):
        # What if data does not contain new_game_name? Throw an exception
        name = data['new_game_name']
        self.shapes[2].set_message(name)  # Not supersure about this
