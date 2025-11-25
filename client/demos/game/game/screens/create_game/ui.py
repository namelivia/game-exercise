from typing import Any, Dict

from engine.api import UIBuilder, UIElementLogic


class NewGameInputCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        name = data["new_game_name"]
        name_text = self.render.find_shape("name")
        if name_text is not None:
            name_text.set_message(name)


def create_new_game_name_input(name: str):
    return (
        UIBuilder(x=20, y=0)
        .with_text("Create a new game", 0, 0)
        .with_text("Please write the name for your new game:", 0, 40)
        .with_text(name, 0, 70, True, "name")
        .with_logic(NewGameInputCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background3.png").build()


def create_error_popup():
    popup = UIBuilder(x=200, y=250).with_text("Error creating game").build()
    popup.hide()
    return popup
