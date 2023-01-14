from client.engine.primitives.command import Command
from .events import (
    PlayerPlacedSymbolInGameEvent,
    PlaceASymbolNetworkRequestEvent,
    SymbolPlacedConfirmedInGameEvent,
    SymbolPlacedErroredEvent,
)


class SymbolPlacedConfirmedCommand(Command):
    # Let the game know that the symbol has been correctly placed
    def __init__(self, profile, queue, event_id):
        super().__init__(profile, queue, f"Symbol placement event {event_id} confirmed")
        self.events = [SymbolPlacedConfirmedInGameEvent(event_id)]


class PlayerPlacedSymbolInGameCommand(Command):
    # Let the game know that there is a new symbol placed on the screen
    def __init__(self, profile, queue, event_id, player_id, position):
        super().__init__(
            profile, queue, f"Player {player_id} placed a symbol on position {position}"
        )
        self.events = [
            PlayerPlacedSymbolInGameEvent(
                player_id, position, "OK", event_id  # This is the original event_id
            )
        ]


class PlaceASymbol(Command):
    # Send a symbol placement to the server
    def __init__(self, profile, queue, game_id, event_id, position):
        super().__init__(
            profile, queue, f"Place a symbol on game {game_id} on position {position}"
        )
        self.events = [PlaceASymbolNetworkRequestEvent(game_id, event_id, position)]


class SymbolPlacedErroredCommand(Command):
    def __init__(self, profile, queue, player_id, event_id):
        super().__init__(profile, queue, f"Symbol place event {event_id} errored")
        self.events = [SymbolPlacedErroredEvent(event_id)]
