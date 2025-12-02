from typing import Any, Dict

from engine.api import UIBuilder, UIElementLogic


class NameInputCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        super().update(time, data)
        name = data["name"]
        name_text = self.render.find_shape("name")
        if name_text is not None:
            name_text.set_message(name)


def create_name_input(name: str):
    return (
        UIBuilder(x=20, y=0)
        .with_text("Set name", 0, 0)
        .with_text("Please enter your player name", 0, 40)
        .with_text(name, 0, 70, True, "name")
        .with_logic(NameInputCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background3.png").build()
