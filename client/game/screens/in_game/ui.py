from client.graphics.shapes import SmallText, Image, Animation
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
            SmallText(str(event), 20, 300 + (20 * index))
            for index, event in enumerate(events)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        events = data["events"]
        self.shapes = [
            SmallText(str(event), 20, 300 + (20 * index))
            for index, event in enumerate(events)
        ]


class EventPointerIndicator(UIElement):
    def __init__(self, event_pointer):
        self.event_pointer = event_pointer
        self.shapes = [SmallText(f"Event pointer at {self.event_pointer}", 20, 200)]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        event_pointer = data["event_pointer"]
        self.shapes = [SmallText(f"Event pointer at {event_pointer}", 20, 200)]


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background5.png", 0, 0)]


class IntroAnimation(UIElement):
    def __init__(self):
        self.shapes = [
            Animation("client/game/images/coin", 0, 150),
            Animation("client/game/images/coin", 250, 0, 3),
        ]

        self.shapes[0].hide()
        self.shapes[1].hide()
        self.timer = 0

    def play(self):
        self.shapes[0].show()
        self.shapes[1].show()
        self.timer = 0

    def update(self, time, data):
        self.timer += 1
        animation_speed = 128  # The higher the slower
        if (time % animation_speed) == 0:
            self.shapes[0].update()  # Not supersure about this
            self.shapes[1].update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x((time / movement_speed) % 640)  # Not supersure about this
        self.shapes[1].set_y((time / movement_speed) % 480)  # Not supersure about this

        if self.timer > 200:
            self.shapes[0].hide()
            self.shapes[1].hide()
