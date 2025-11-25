from typing import Any, Dict

from engine.api import UIBuilder, UIElementLogic


class WelcomeMessageCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        welcome_text = self.render.find_shape("welcome")
        if welcome_text is not None:
            message = f"Welcome to game, {data['player_name']}"
            welcome_text.set_message(message)


def create_welcome_message():
    return (
        UIBuilder(x=20, y=0)
        .with_text("Welcome to game", 0, 0, True, "welcome")
        .with_logic(WelcomeMessageCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background2.png").build()


def create_options(options: Dict[str, str]):
    builder = UIBuilder(x=20, y=50)
    for index, option in options.items():
        builder.with_text(f"{index} - {option}", 0, 20 * int(index))
    return builder.build()
