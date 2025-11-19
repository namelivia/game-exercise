from typing import TYPE_CHECKING

from engine.primitives.command import Command

from .events import (
    PlayMusicEvent,
    PlaySoundEvent,
    StopMusicEvent,
    TurnSoundOffEvent,
    TurnSoundOnEvent,
)


class PlaySound(Command):
    def __init__(self, sound_id: str) -> None:
        super().__init__(f"Playing sound {sound_id}")
        self.queue = "sound"
        self.events = [
            PlaySoundEvent(sound_id),
        ]


class PlayMusic(Command):
    def __init__(self, music_id: str) -> None:
        super().__init__(f"Playing music {music_id}")
        self.queue = "sound"
        self.events = [
            PlayMusicEvent(music_id),
        ]


class StopMusic(Command):
    def __init__(self) -> None:
        super().__init__(f"Stopping music")
        self.queue = "sound"
        self.events = [
            StopMusicEvent(),
        ]


class TurnSoundOn(Command):
    def __init__(self) -> None:
        super().__init__(f"Turning sound on")
        self.queue = "sound"
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self) -> None:
        super().__init__(f"Turning sound off")
        self.queue = "sound"
        self.events = [
            TurnSoundOffEvent(),
        ]
