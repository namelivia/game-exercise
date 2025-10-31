from client.engine.graphics.shapes import Image, Text
from client.engine.primitives.ui import UIElement


class CreditsUI(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Credits", 100, 100),
            Text("@namelivia", 100, 150),
        ]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]
