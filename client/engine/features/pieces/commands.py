from typing import TYPE_CHECKING

from client.engine.primitives.command import Command

from .events import (
    PlaceASymbolNetworkRequestEvent,
    PlayerPlacedSymbolInGameEvent,
    SymbolPlacedConfirmedInGameEvent,
    SymbolPlacedErroredEvent,
)

if TYPE_CHECKING:
    from uuid import UUID

    from client.engine.general_state.queue import Queue


class SymbolPlacedConfirmedCommand(Command):
    # Let the game know that the symbol has been correctly placed
    def __init__(self, queue: "Queue", event_id: "UUID"):
        super().__init__(queue, f"Symbol placement event {event_id} confirmed")
        self.events = [SymbolPlacedConfirmedInGameEvent(event_id)]


class PlayerPlacedSymbolInGameCommand(Command):
    # Let the game know that there is a new symbol placed on the screen
    def __init__(
        self,
        queue: "Queue",
        event_id: "UUID",
        player_id: "UUID",
        position: int,
    ):
        super().__init__(
            queue, f"Player {player_id} placed a symbol on position {position}"
        )
        self.events = [
            PlayerPlacedSymbolInGameEvent(
                player_id, position, "OK", event_id  # This is the original event_id
            )
        ]


class PlaceASymbol(Command):
    # Send a symbol placement to the server
    def __init__(
        self,
        queue: "Queue",
        game_id: "UUID",
        event_id: "UUID",
        position: int,
    ):
        super().__init__(
            queue, f"Place a symbol on game {game_id} on position {position}"
        )
        self.events = [PlaceASymbolNetworkRequestEvent(game_id, event_id, position)]


class SymbolPlacedErroredCommand(Command):
    # Let the game know that the symbol was not correctly placed and needs to be rolled back
    def __init__(self, queue: "Queue", event_id: "UUID"):
        super().__init__(queue, f"Symbol place event {event_id} errored")
        self.events = [SymbolPlacedErroredEvent(event_id)]
