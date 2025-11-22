from typing import Any, Dict

from engine.api import Image, create_ui_element

"""
class EnterNameMessage(UIElement):
    def __init__(self, name: str):
        self.name = name
        self.shapes = [
            Text("Set name", 20, 0),
            Text("Please enter your player name:", 20, 40),
            Text(name, 20, 70),
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain new_game_name? Throw an exception
        name = data["name"]
        name_text = self.shapes[2]
        if isinstance(name_text, Text):
            name_text.set_message(name)  # Not supersure about this
"""


def create_background():
    return create_ui_element([Image("assets/images/background3.png", 0, 0)])
