from typing import Dict

from engine.api import Text, UIBuilder, create_ui_element


def create_title():
    return create_ui_element([Text("Options", 20, 0)])


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()


def create_options(options: Dict[str, str]):
    shapes = []
    for index, option in options.items():
        shapes.append(Text(f"{index} - {option}", 20, 200 + (30 * int(index))))
    return create_ui_element(shapes)
