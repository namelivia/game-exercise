from typing import Dict

from client.engine.graphics.shapes import Image, Text
from client.engine.primitives.ui import UIElement


class WelcomeMessage(UIElement):
    def __init__(self, name: str, id: str):
        self.name = name
        self.name = id
        self.shapes = [Text(f"Welcome to game, {name} {id}", 20, 0)]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background2.png", 0, 0)]


class OptionList(UIElement):
    def __init__(self, options: Dict[str, str]):
        self.options = options
        self.shapes = []
        for index, option in self.options.items():
            self.shapes.append(Text(f"{index} - {option}", 20, 200 + (30 * int(index))))
