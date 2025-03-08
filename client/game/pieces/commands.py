from typing import TYPE_CHECKING

from client.engine.features.pieces.events import PlayerPlacedSymbolInGameEvent
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.primitives.command import Command

from .events import PlaceASymbolRequestEvent

if TYPE_CHECKING:
    from client.engine.general_state.queue import Queue

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class RequestPlaceASymbol(Command):
    def __init__(self, queue: "Queue", position: int):
        super().__init__(queue, f"Request placing a symbol on position {position}")
        # We need to attach the in_game event id to the network request
        profile_what = ProfileWhat()
        in_game_event = PlayerPlacedSymbolInGameEvent(
            profile_what.profile.id, int(position), "pending"
        )
        self.events = [
            in_game_event,
            PlaceASymbolRequestEvent(in_game_event.id, position),
        ]
