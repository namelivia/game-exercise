from client.engine.graphics.shapes import Text, Image
from client.engine.primitives.ui import UIElement


class GameIdMessage(UIElement):
    def __init__(self, game_id):
        self.game_id = game_id
        self.shapes = [
            Text("Join an existing game", 20, 0),
            Text("Please write the id for the game:", 20, 40),
            Text(game_id, 20, 70),
        ]

    def update(self, time, data):
        # What if data does not contain game_id? Throw an exception
        game_id = data["game_id"]
        self.shapes[2].set_message(game_id)  # Not supersure about this


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class ErrorPopup(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Error Joining Game", 200, 250),
        ]

        self.shapes[0].hide()

    def show(self):
        self.shapes[0].show()


class ErrorJoiningPopup(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Error Joining Game", 200, 250),
        ]

        self.shapes[0].hide()

    def show(self):
        self.shapes[0].show()
