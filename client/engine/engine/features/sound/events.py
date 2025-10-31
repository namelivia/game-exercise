from engine.primitives.event import Event


class PlaySoundEvent(Event):
    def __init__(self, sound: str):
        super().__init__()
        self.sound = sound


class PlayMusicEvent(Event):
    def __init__(self, music: str):
        super().__init__()
        self.music = music


class StopMusicEvent(Event):
    def __init__(self):
        super().__init__()
