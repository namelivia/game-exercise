from client.engine.primitives.event import Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class ScreenTransitionEvent(Event):
    def __init__(self, dest_screen):
        super().__init__()
        self.dest_screen = dest_screen


class ClearInternalGameInformationEvent:
    pass


class PlaySoundEvent(Event):
    def __init__(self, sound):
        super().__init__()
        self.sound = sound


class PlayMusicEvent(Event):
    def __init__(self, music):
        super().__init__()
        self.music = music
