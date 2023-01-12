from client.engine.primitives.command import Command
from .events import (
    TurnSoundOnEvent,
    TurnSoundOffEvent,
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
