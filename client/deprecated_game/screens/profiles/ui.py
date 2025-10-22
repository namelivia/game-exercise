from typing import Any, Dict, List

from client.engine.graphics.shapes import Image, SmallText, Text
from client.engine.primitives.ui import UIElement


class ProfilesTitle(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Text("Profiles", 20, 0),
        ]


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/game/images/background4.png", 0, 0)]


class ProfileList(UIElement):
    def _build_profile_entry(self, name: str, index: int) -> str:
        return str(index + 1) + " - " + name

    def _get_profile_entry_y(self, index: int) -> int:
        return 50 + (20 * (index + 1))

    def __init__(self, profiles: List[Dict[str, str]]):
        self.profiles = profiles
        self.shapes = [SmallText("0 - New profile", 20, 50)]
        self.shapes += [
            SmallText(
                self._build_profile_entry(profile["name"], index),
                20,
                self._get_profile_entry_y(index),
            )
            for index, profile in enumerate(profiles)
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        # What if data does not contain profiles? Throw an exception
        profiles = data["profiles"]
        self.shapes = [SmallText("0 - New profile", 20, 50)]
        self.shapes += [
            SmallText(
                self._build_profile_entry(profile["name"], index),
                20,
                self._get_profile_entry_y(index),
            )
            for index, profile in enumerate(profiles)
        ]
