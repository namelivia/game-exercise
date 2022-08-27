from client.engine.graphics.shapes import Text, Image, SmallText
from client.engine.primitives.ui import UIElement


class ProfilesTitle(UIElement):
    def __init__(self):
        self.shapes = [
            Text("Profiles", 20, 0),
        ]


class Background(UIElement):
    def __init__(self):
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class ProfileList(UIElement):
    def __init__(self, profiles):
        self.profiles = profiles
        self.shapes = [
            SmallText("0 - New profile", 20, 50)
        ]
        self.shapes += [
            SmallText(str(index + 1) + " - " + str(event["name"]), 20, 50 + (20 * (index + 1)))
            for index, event in enumerate(profiles)
        ]

    def update(self, time, data):
        # What if data does not contain events? Throw an exception
        profiles = data["profiles"]
        self.shapes = [
            SmallText("0 - New profile", 20, 50)
        ]
        self.shapes += [
            SmallText(str(index + 1) + " - " + str(event["name"]), 20, 50 + (20 * (index + 1)))
            for index, event in enumerate(profiles)
        ]
