from typing import Any, Dict

from engine.api import UIBuilder, UIElementLogic


class TitleCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        super().update(time, data)
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.state.set_x(int((time / inverse_speed) % (640 + offset) - offset))


def create_title():
    return (
        UIBuilder(x=20, y=10)
        .with_text("Welcome to the game")
        .with_logic(TitleCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background.png").build()


def create_coin_1():
    coin = (
        UIBuilder(x=150, y=150)
        .with_animation("assets/images/coin.json", 0, 0, 30)
        .build()
    )
    return coin


def create_coin_2():
    coin = (
        UIBuilder(x=90, y=100)
        .with_animation("assets/images/coin.json", 0, 0, 15)
        .build()
    )
    return coin
