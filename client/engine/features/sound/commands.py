from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import PlayMusicEvent, PlaySoundEvent, TurnSoundOffEvent, TurnSoundOnEvent

if TYPE_CHECKING:
    from client.engine.general_state.queue import Queue


class TurnSoundOn(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Turning sound ON")
        self.events = [
            TurnSoundOnEvent(),
        ]


class TurnSoundOff(Command):
    def __init__(self, queue: "Queue"):
        super().__init__(queue, "Turning sound OFF")
        self.events = [
            TurnSoundOffEvent(),
        ]


class PlaySound(Command):
    def __init__(self, queue: "Queue", sound_id: str):
        super().__init__(queue, f"Playing sound {sound_id}")
        self.events = [
            PlaySoundEvent(sound_id),
        ]


class PlayMusic(Command):
    def __init__(self, queue: "Queue", music_id: str):
        super().__init__(queue, f"Playing music {music_id}")
        self.events = [
            PlayMusicEvent(music_id),
        ]
