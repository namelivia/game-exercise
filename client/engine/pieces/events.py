from client.engine.primitives.event import InGameEvent, Event

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class PlayerPlacedSymbolInGameEvent(InGameEvent):
    def __init__(self, player_id, position):
        super().__init__()
        self.player_id = player_id
        self.position = position


class PlaceASymbolNetworkRequestEvent(Event):
    def __init__(self, game_id, event_id, position):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.position = position
