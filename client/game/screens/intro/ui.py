from typing import Any, Dict

from client.engine.animation_factory import create_animation
from client.engine.graphics.shapes import Animation, Image, Text
from client.engine.primitives.ui import (
    UIElementLogic,
    UIElementState,
    create_ui_element,
)

"""
class Title(UIElement):
    def __init__(self) -> None:
        self.shapes = [Text("Welcome to the game", 20, 10)]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.shapes[0].set_x(
            int((time / inverse_speed) % (640 + offset) - offset)
        )  # Not supersure about this
"""


class TitleCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.state.set_x(
            int((time / inverse_speed) % (640 + offset) - offset)
        )  # Not supersure about this


def create_title():
    state = UIElementState(20, 10)
    return create_ui_element(
        [Text("Welcome to the game", 0, 0)], state, TitleCustomLogic(state)
    )


def create_background():
    return create_ui_element([Image("client/game/images/background.png", 0, 0)])


def create_coin_1():
    coin = create_animation("client/game/images/coin.json", 150, 150, 30)
    coin.hide()
    return coin


def create_coin_2():
    coin = create_animation("client/game/images/coin.json", 90, 100, 15)
    coin.hide()
    return coin


"""
class Coins(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Animation("client/game/images/coin", 0, 150),
            Animation("client/game/images/coin", 250, 0, 3),
        ]

        self.shapes[0].hide()
        self.shapes[1].hide()

    def update(self, time: int, data: Dict[str, Any]) -> None:
        animation_speed = 128  # The higher the slower
        if (time % animation_speed) == 0:
            animation_1 = self.shapes[0]
            animation_2 = self.shapes[1]
            if isinstance(animation_1, Animation) and isinstance(
                animation_2, Animation
            ):
                animation_1.update()  # Not supersure about this
                animation_2.update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x(
            int((time / movement_speed) % 640)
        )  # Not supersure about this
        self.shapes[1].set_y(
            int((time / movement_speed) % 480)
        )  # Not supersure about this
"""
