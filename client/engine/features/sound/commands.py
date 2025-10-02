from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import (
    PlayMusicEvent,
    PlaySoundEvent,
    StopMusicEvent,
    TurnSoundOffEvent,
    TurnSoundOnEvent,
)


class TurnSoundOn(Command):
    def __init__(self) -> None:
        super().__init__("Turning sound ON")
        self.queue = "sound"
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self) -> None:
        super().__init__("Turning sound OFF")
        self.queue = "sound"
        self.events = [
            TurnSoundOffEvent(),
        ]


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
