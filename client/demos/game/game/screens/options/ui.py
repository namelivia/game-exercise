from typing import Dict

from engine.api import Image, Text, create_ui_element


def create_title():
    return create_ui_element([Text("Options", 20, 0)])


def create_background():
    return create_ui_element([Image("assets/images/background4.png", 0, 0)])


def create_options(options: Dict[str, str]):
    shapes = []
    for index, option in options.items():
        shapes.append(Text(f"{index} - {option}", 20, 200 + (30 * int(index))))
    return create_ui_element(shapes)
