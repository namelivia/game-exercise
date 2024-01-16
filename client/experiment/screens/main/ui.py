from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import UIElement


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/experiment/images/background.png", 0, 0)]
