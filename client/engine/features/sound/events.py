from client.engine.primitives.event import Event


class TurnSoundOnEvent(Event):
    pass


class TurnSoundOffEvent(Event):
    pass


class PlaySoundEvent(Event):
    def __init__(self, sound):
        super().__init__()
        self.sound = sound


class PlayMusicEvent(Event):
    def __init__(self, music):
        super().__init__()
        self.music = music
