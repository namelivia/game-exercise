from client.engine.primitives.command import Command
from client.engine.features.pieces.events import (
    PlayerPlacedSymbolInGameEvent,
)
from .events import PlaceASymbolRequestEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class RequestPlaceASymbol(Command):
    def __init__(self, profile, queue, position):
        super().__init__(
            profile, queue, f"Request placing a symbol on position {position}"
        )
        # We need to attach the in_game event id to the network request
        in_game_event = PlayerPlacedSymbolInGameEvent(
            profile.id, int(position), "pending"
        )
        self.events = [
            in_game_event,
            PlaceASymbolRequestEvent(in_game_event.id, position),
        ]
