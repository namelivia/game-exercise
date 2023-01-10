from client.engine.primitives.command import Command
from .events import PlayerPlacedSymbolInGameEvent, PlaceASymbolNetworkRequestEvent

"""
Commands are called externally, and are defined by 1 or many events.
When the commands are executed these events are placed on the queue to be
processed.
"""


class PlayerPlacedSymbolInGameCommand(Command):
    def __init__(self, profile, queue, player_id, position):
        super().__init__(
            profile, queue, f"Player {player_id} placed a symbol on position {position}"
        )
        self.events = [
            PlayerPlacedSymbolInGameEvent(
                player_id, position
            )  # Event to be picked up by the screen event handler
            # I should pick this event on the game but
            # Still don't do anything with this event
        ]


class PlaceASymbol(Command):
    def __init__(self, profile, queue, game_id, event_id, position):
        super().__init__(
            profile, queue, f"Place a symbol on game {game_id} on position {position}"
        )
        self.events = [PlaceASymbolNetworkRequestEvent(game_id, event_id, position)]
