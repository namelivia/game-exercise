from client.engine.graphics.shapes import Text, Image, Animation
from client.engine.primitives.ui import UIElement


class Title(UIElement):
    def __init__(self, value):
        self.shapes = [Text("Welcome to the game", 20, 10)]

    def update(self, time, data):
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.shapes[0].set_x(
            (time / inverse_speed) % (640 + offset) - offset
        )  # Not supersure about this


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background.png", 0, 0)]


class Coins(UIElement):
    def __init__(self):
        self.shapes = [
            Animation("client/game/images/coin", 0, 150),
            Animation("client/game/images/coin", 250, 0, 3),
        ]

        self.shapes[0].hide()
        self.shapes[1].hide()

    def appear(self):
        self.shapes[0].show()
        self.shapes[1].show()

    def update(self, time, data):
        animation_speed = 128  # The higher the slower
        if (time % animation_speed) == 0:
            self.shapes[0].update()  # Not supersure about this
            self.shapes[1].update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x((time / movement_speed) % 640)  # Not supersure about this
        self.shapes[1].set_y((time / movement_speed) % 480)  # Not supersure about this
