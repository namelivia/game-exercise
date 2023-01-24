from typing import Optional
from client.engine.primitives.event import InGameEvent, Event


class SymbolPlacedConfirmedInGameEvent(InGameEvent):
    def __init__(self, place_symbol_event_id: str):
        super().__init__()
        self.place_symbol_event_id = place_symbol_event_id


class PlayerPlacedSymbolInGameEvent(InGameEvent):
    def __init__(
        self,
        player_id: str,
        position: int,
        confirmation: str,
        original_event_id: Optional[str] = None,
    ):
        super().__init__()
        self.player_id = player_id
        self.position = position
        self.confirmation = confirmation
        self.original_event_id = original_event_id


class PlaceASymbolNetworkRequestEvent(Event):
    def __init__(self, game_id: str, event_id: str, position: int):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.position = position


class SymbolPlacedErroredEvent(InGameEvent):
    # This indicates that a chat message wasn't sucessfully processed
    # by the server and therefore it needs to be rolled back.
    def __init__(self, place_symbol_event_id: str):
        super().__init__()
        self.place_symbol_event_id = place_symbol_event_id
