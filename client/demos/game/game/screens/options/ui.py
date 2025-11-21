from typing import Dict

from engine.api import UIBuilder


def create_title():
    return UIBuilder(x=20, y=0).with_text("Options").build()


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()


def create_options(options: Dict[str, str]):
    builder = UIBuilder(x=20, y=50)
    for index, option in options.items():
        builder.with_text(f"{index} - {option}", 0, 30 * int(index))
    return builder.build()
