from typing import TYPE_CHECKING, Any, Dict

from engine.api import UIBuilder, UIElementLogic


class GameIdInputCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        name = data["game_id"]
        id_text = self.render.find_shape("game_id")
        if id_text is not None:
            id_text.set_message(name)


def create_game_id_input(name: str):
    return (
        UIBuilder(x=20, y=0)
        .with_text("Join an existing game", 0, 0)
        .with_text("Please write the id for your the game:", 0, 40)
        .with_text(name, 0, 70, True, "game_id")
        .with_logic(GameIdInputCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()


def create_error_popup():
    popup = UIBuilder(x=200, y=250).with_text("Error joining game").build()
    popup.hide()
    return popup
