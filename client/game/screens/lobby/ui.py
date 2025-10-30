from typing import Dict

from client.engine.graphics.shapes import Image, Text
from client.engine.primitives.ui import UIElement, create_ui_element


def create_welcome_message():
    return create_ui_element([Text("Welcome to game", 20, 0)])


def create_background():
    return create_ui_element([Image("client/game/images/background2.png", 0, 0)])


def create_options(options: Dict[str, str]):
    shapes = []
    for index, option in options.items():
        shapes.append(Text(f"{index} - {option}", 20, 200 + (30 * int(index))))
    return create_ui_element(shapes)
