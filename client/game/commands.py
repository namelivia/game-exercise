from typing import TYPE_CHECKING

from client.engine.features.sound.events import PlaySoundEvent
from client.engine.primitives.command import Command

from .events import ClearInternalGameInformationEvent, ScreenTransitionEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self) -> None:
        super().__init__("Move back to lobby")
        self.events = [
            ClearInternalGameInformationEvent(),
            PlaySoundEvent("client/game/sounds/back.mp3"),
            ScreenTransitionEvent("lobby"),
        ]


class ToLobby(Command):
    def __init__(self) -> None:
        super().__init__("Move forward to lobby")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("lobby"),
        ]


class NewGame(Command):
    def __init__(self) -> None:
        super().__init__("Move to new game screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("new_game_screen"),
        ]


class GoToJoinAGame(Command):
    def __init__(self) -> None:
        super().__init__("Move to join game screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("join_a_game"),
        ]


class GoToGameList(Command):
    def __init__(self) -> None:
        super().__init__("Move to game list screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("game_list"),
        ]


class GoToOptions(Command):
    def __init__(self) -> None:
        super().__init__("Move to options screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("options"),
        ]


class GoToCredits(Command):
    def __init__(self) -> None:
        super().__init__("Move to options screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("credits"),
        ]


class GoToSetName(Command):
    def __init__(self) -> None:
        super().__init__("Move to set name screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("enter_name"),
        ]


class GoToProfiles(Command):
    def __init__(self) -> None:
        super().__init__("Move to the profiles screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("profiles"),
        ]
