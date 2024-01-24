from typing import TYPE_CHECKING

from client.engine.features.sound.events import PlaySoundEvent
from client.engine.primitives.command import Command

from .events import ClearInternalGameInformationEvent, ScreenTransitionEvent

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move back to lobby")
        self.events = [
            ClearInternalGameInformationEvent(),
            PlaySoundEvent("client/game/sounds/back.mp3"),
            ScreenTransitionEvent("lobby"),
        ]


class ToLobby(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move forward to lobby")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("lobby"),
        ]


class NewGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to new game screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("new_game_screen"),
        ]


class GoToJoinAGame(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to join game screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("join_a_game"),
        ]


class GoToGameList(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to game list screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("game_list"),
        ]


class GoToOptions(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to options screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("options"),
        ]


class GoToCredits(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to options screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("credits"),
        ]


class GoToSetName(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to set name screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("enter_name"),
        ]


class GoToProfiles(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Move to the profiles screen")
        self.events = [
            PlaySoundEvent("client/game/sounds/select.mp3"),
            ScreenTransitionEvent("profiles"),
        ]
