from typing import TYPE_CHECKING

from engine.features.pieces.events import PlayerPlacedSymbolInGameEvent
from engine.general_state.profile_manager import ProfileManager
from engine.primitives.command import Command

from .events import PlaceASymbolRequestEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class RequestPlaceASymbol(Command):
    def __init__(self, position: int):
        super().__init__(f"Request placing a symbol on position {position}")
        # We need to attach the in_game event id to the network request
        profile_manager = ProfileManager()
        in_game_event = PlayerPlacedSymbolInGameEvent(
            profile_manager.profile.id, int(position), "pending"
        )
        self.events = [
            in_game_event,
            PlaceASymbolRequestEvent(in_game_event.id, position),
        ]
