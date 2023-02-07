from typing import TYPE_CHECKING, Any, Dict

from client.engine.graphics.shapes import Image, Text
from client.engine.primitives.ui import UIElement

if TYPE_CHECKING:
    from uuid import UUID


class GameIdMessage(UIElement):
    def __init__(self, game_id: "UUID"):
        self.game_id = game_id
        self.shapes = [
            Text("Join an existing game", 20, 0),
            Text("Please write the id for the game:", 20, 40),
            Text(str(game_id), 20, 70),
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain game_id? Throw an exception
        game_id = data["game_id"]
        game_id_text = self.shapes[2]
        if isinstance(game_id_text, Text):
            game_id_text.set_message(game_id)  # Not supersure about this


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class ErrorPopup(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Error Joining Game", 200, 250),
        ]

        self.shapes[0].hide()


class ErrorJoiningPopup(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Error Joining Game", 200, 250),
        ]

        self.shapes[0].hide()
