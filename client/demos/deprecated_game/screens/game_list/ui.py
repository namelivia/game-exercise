from typing import Any, Dict, List

from client.engine.graphics.shapes import Image, SmallText, Text
from client.engine.primitives.ui import UIElement


class GameListTitle(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Game List", 20, 0),
        ]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class Games(UIElement):
    def __init__(self, games: List[Any]):
        self.games = games
        self.shapes = [
            SmallText(str(index) + " - " + str(game.name), 20, 50 + (20 * index))
            for index, game in enumerate(games)
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain events? Throw an exception
        games = data["games"]
        self.shapes = [
            SmallText(str(index) + " - " + str(game.name), 20, 50 + (20 * index))
            for index, game in enumerate(games)
        ]


class ErrorPopup(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Error Getting Game List", 200, 250),
        ]

        self.shapes[0].hide()


class ErrorJoiningPopup(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Error Joining Game", 200, 250),
        ]

        self.shapes[0].hide()
