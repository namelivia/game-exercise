from client.engine.graphics.shapes import Text, Image, SmallText
from client.engine.primitives.ui import UIElement


class GameListTitle(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Game List", 20, 0),
        ]


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class Games(UIElement):
    def __init__(self, games):
        self.games = games
        self.shapes = [
            SmallText(str(index) + " - " + str(event.name), 20, 50 + (20 * index))
            for index, event in enumerate(games)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        games = data["games"]
        self.shapes = [
            SmallText(str(index) + " - " + str(event.name), 20, 50 + (20 * index))
            for index, event in enumerate(games)
        ]


class ErrorPopup(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Error Getting Game List", 200, 250),
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
