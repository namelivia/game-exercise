from client.graphics.shapes import Text, Image, SmallText
from client.primitives.ui import UIElement


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
            SmallText(str(event), 20, 50 + (20 * index))
            for index, event in enumerate(games)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        games = data["games"]
        self.shapes = [
            SmallText(str(event), 20, 50 + (20 * index))
            for index, event in enumerate(games)
        ]
