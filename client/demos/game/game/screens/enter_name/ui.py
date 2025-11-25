from typing import Any, Dict

from engine.api import UIBuilder, UIElementLogic


class NameInputCustomLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        name = data["name"]
        # name_text = self.shapes[2]
        # if isinstance(name_text, Text):
        # name_text.set_message(name)  # Not supersure about this


def create_name_input(name: str):
    return (
        UIBuilder(x=20, y=0)
        .with_text("Set name", 0, 0)
        .with_text("Please enter your player name", 0, 40)
        .with_text(name, 0, 70)
        .with_logic(NameInputCustomLogic)
        .build()
    )


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background3.png").build()
