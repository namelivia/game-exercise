from client.engine.primitives.command import Command
from .events import (
    TurnSoundOnEvent,
    TurnSoundOffEvent,
    PlaySoundEvent,
    PlayMusicEvent,
)


class TurnSoundOn(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Turning sound ON")
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self, profile, queue):
        super().__init__(profile, queue, "Turning sound OFF")
        self.events = [
            TurnSoundOffEvent(),
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
