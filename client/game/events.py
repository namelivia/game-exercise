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


class PlaceASymbolRequestEvent(Event):
    def __init__(self, position):
        super().__init__()
        self.position = position


class SendChatRequestEvent(Event):
    def __init__(self, event_id, message):
        super().__init__()
        self.event_id = event_id
        self.message = message


class SendChatNetworkRequestEvent(Event):
    def __init__(self, game_id, event_id, message):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.message = message


class ClearInternalGameInformationEvent:
    pass


class PlaceASymbolNetworkRequestEvent(Event):
    def __init__(self, game_id, position):
        super().__init__()
        self.game_id = game_id
        self.position = position


class PlaySoundEvent(Event):
    def __init__(self, sound):
        super().__init__()
        self.sound = sound


class PlayMusicEvent(Event):
    def __init__(self, music):
        super().__init__()
        self.music = music
