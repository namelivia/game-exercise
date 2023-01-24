from typing import TYPE_CHECKING
from client.engine.primitives.command import Command
from .events import (
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    PlaySoundEvent,
    PlayMusicEvent,
)

if TYPE_CHECKING:
    from client.engine.general_state.profile.profile import Profile
    from client.engine.general_state.queue import Queue


class TurnSoundOn(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Turning sound ON")
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self, profile: "Profile", queue: "Queue"):
        super().__init__(profile, queue, "Turning sound OFF")
        self.events = [
            TurnSoundOffEvent(),
        ]


class PlaySound(Command):
    def __init__(self, profile: "Profile", queue: "Queue", sound_id: str):
        super().__init__(profile, queue, f"Playing sound {sound_id}")
        self.events = [
            PlaySoundEvent(sound_id),
        ]


class PlayMusic(Command):
    def __init__(self, profile: "Profile", queue: "Queue", music_id: str):
        super().__init__(profile, queue, f"Playing music {music_id}")
        self.events = [
            PlayMusicEvent(music_id),
        ]
