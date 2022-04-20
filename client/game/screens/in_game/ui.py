from client.graphics.shapes import SmallText, Image
from client.primitives.ui import UIElement


class GameIdIndicator(UIElement):
    def __init__(self, game_id):
        self.game_id = game_id
        self.shapes = [SmallText(f"Game Id: {game_id}", 20, 40)]


class GameNameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [SmallText(f"Game name: {name}", 20, 60)]


class Player1NameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [SmallText(f"Player 1 name: {name}", 20, 80)]


class Player2NameIndicator(UIElement):
    def __init__(self, name):
        self.name = name
        self.shapes = [SmallText(f"Player 2 name: {name}", 20, 100)]


class Events(UIElement):
    def __init__(self, events):
        self.events = events
        self.shapes = [
            SmallText(event, 20, 300 + (20 * index))
            for index, event in enumerate(events)
        ]


class Instructions(UIElement):
    def __init__(self):
        self.shapes = [SmallText("Press the square number to place a symbol", 20, 200)]


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background5.png", 0, 0)]
