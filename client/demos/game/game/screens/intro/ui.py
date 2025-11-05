from typing import Any, Dict

from engine.api import (
    Image,
    Text,
    UIElementLogic,
    UIElementState,
    create_animation,
    create_ui_element,
)


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
    return create_ui_element([Image("assets/images/background.png", 0, 0)])


def create_coin_1():
    coin = create_animation("assets/images/coin.json", 150, 150, 30)
    coin.hide()
    return coin


def create_coin_2():
    coin = create_animation("assets/images/coin.json", 90, 100, 15)
    coin.hide()
    return coin
