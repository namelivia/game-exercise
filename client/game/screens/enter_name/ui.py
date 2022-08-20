from client.engine.graphics.shapes import Text, Image
from client.engine.primitives.ui import UIElement


class EnterNameMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text("Set name", 20, 0),
            Text("Please enter your player name:", 20, 40),
            Text(name, 20, 70),
        ]

    def update(self, time, data):
        # What if data does not contain new_game_name? Throw an exception
        name = data["name"]
        self.shapes[2].set_message(name)  # Not supersure about this


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background3.png", 0, 0)]
