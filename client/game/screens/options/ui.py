from client.engine.graphics.shapes import Text, Image
from client.engine.primitives.ui import UIElement
from typing import Dict


class OptionsTitle(UIElement):
    def __init__(self) -> None:
        self.shapes = [Text("Options", 20, 0)]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class OptionList(UIElement):
    def __init__(self, options: Dict[str, str]) -> None:
        self.options = options
        self.shapes = []
        for index, option in self.options.items():
            self.shapes.append(Text(f"{index} - {option}", 20, 200 + (30 * int(index))))
