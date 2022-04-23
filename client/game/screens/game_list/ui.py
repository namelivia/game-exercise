from client.graphics.shapes import Text, Image
from client.primitives.ui import UIElement


class GameListTitle(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Game List", 20, 0),
        ]


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]
