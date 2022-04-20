from client.primitives.event import Event

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
