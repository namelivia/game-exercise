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
        self.shapes = [SmallText(f"Player 1 name: {name}", 20, 80)]


class Player2NameIndicator(UIElement):
    def __init__(self, name):
        self.shapes = [SmallText(f"Player 2 name: {name}", 20, 100)]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        name = data["players"][1]
        self.shapes = [SmallText(f"Player 2 name: {name}", 20, 100)]


class Events(UIElement):
    def _get_event_string(self, event, pointer, index):
        return str(event) + " <= [POINTER]" if index == pointer else str(event)

    def __init__(self, events, pointer):
        self.events = events
        self.shapes = [
            SmallText(self._get_event_string(event, pointer, index), 20, 300 + (20 * index))
            for index, event in enumerate(events)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        events = data["events"]
        pointer = data["event_pointer"]
        self.shapes = [
            SmallText(self._get_event_string(event, pointer, index), 20, 300 + (20 * index))
            for index, event in enumerate(events)
        ]


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


class ChatInput(UIElement):
    def __init__(self):
        self.shapes = [SmallText("Send message: ", 20, 450)]
        self.visible = False

    def focus(self):
        self.visible = True

    def unfocus(self):
        self.visible = False

    def update(self, time, data):
        if self.visible:
            # What if data does not contain events? Throw an exception
            self.shapes = [SmallText(f"Send message: {data['chat_input']}", 20, 450)]
        else:
            self.shapes = []
