from client.primitives.command import Command
from .events import (
    ScreenTransitionEvent,
    PlaceASymbolRequestEvent,
    PlaceASymbolNetworkRequestEvent,
    ClearInternalGameInformationEvent,
    PlaySoundEvent,
    PlayMusicEvent,
)

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


# These put events on the queue requesting server interactions.
# ===== REQUESTS =====
class RequestPlaceASymbol(Command):
    def __init__(self, profile, queue, position):
        super().__init__(
            profile, queue, f"Request placing a symbol on position {position}"
        )
        self.events = [PlaceASymbolRequestEvent(position)]


# ===== SCREEN CHANGE REQUESTS =====
class BackToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move back to lobby")
        self.events = [
            ClearInternalGameInformationEvent(),
            PlaySoundEvent("back"),
            ScreenTransitionEvent("lobby"),
        ]


class ToLobby(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move forward to lobby")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("lobby"),
        ]


class PlaySound(Command):
    def __init__(self, profile, queue, sound_id):
        super().__init__(profile, queue, f"Playing sound {sound_id}")
        self.events = [
            PlaySoundEvent(sound_id),
        ]


class PlayMusic(Command):
    def __init__(self, profile, queue, music_id):
        super().__init__(profile, queue, f"Playing music {music_id}")
        self.events = [
            PlayMusicEvent(music_id),
        ]


class NewGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to new game screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("new_game_screen"),
        ]


class GoToJoinAGame(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to join game screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("join_a_game"),
        ]


class GoToOptions(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Move to options screen")
        self.events = [
            PlaySoundEvent("select"),
            ScreenTransitionEvent("options"),
        ]


# ===== SERVER OUTBOUND COMMUNICATIONS =====
class PlaceASymbol(Command):
    def __init__(self, profile, queue, game_id, position):
        super().__init__(
            profile, queue, f"Place a symbol on game {game_id} on position {position}"
        )
        self.events = [PlaceASymbolNetworkRequestEvent(game_id, position)]
