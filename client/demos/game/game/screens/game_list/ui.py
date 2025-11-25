from typing import Any, Dict, List

from engine.api import UIBuilder, UIElementLogic


def create_title():
    return UIBuilder(x=20, y=0).with_text("Game List", 0, 0).build()


def create_background():
    return UIBuilder(x=0, y=0).with_image("assets/images/background4.png").build()


# class Games(UIElement):
#    def __init__(self, games: List[Any]):
#        self.games = games
#        self.shapes = [
#            SmallText(str(index) + " - " + str(game.name), 20, 50 + (20 * index))
#            for index, game in enumerate(games)
#        ]
#
#    def update(self, time: int, data: Dict[str, Any]) -> None:
#        # What if data does not contain events? Throw an exception
#        games = data["games"]
#        self.shapes = [
#            SmallText(str(index) + " - " + str(game.name), 20, 50 + (20 * index))
#            for index, game in enumerate(games)
#        ]


def create_error_popup():
    popup = UIBuilder(x=200, y=250).with_text("Error getting game list").build()
    popup.hide()
    return popup


def create_cant_join_popup():
    popup = UIBuilder(x=200, y=250).with_text("Error joining game").build()
    popup.hide()
    return popup
