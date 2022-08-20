from client.graphics.shapes import Text, Image
from client.engine.primitives.ui import UIElement


class NewGameMessage(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [
            Text("Create a new game", 20, 0),
            Text("Please write the name for your new game:", 20, 40),
            Text(name, 20, 70),
        ]

    def update(self, time, data):
        # What if data does not contain new_game_name? Throw an exception
        name = data["new_game_name"]
        self.shapes[2].set_message(name)  # Not supersure about this


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background3.png", 0, 0)]


class ErrorPopup(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Error Creating Game", 200, 250),
        ]

        self.shapes[0].hide()

    def show(self):
        self.shapes[0].show()
