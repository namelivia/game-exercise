from client.engine.primitives.event import InGameEvent, Event


class SymbolPlacedConfirmedInGameEvent(InGameEvent):
    def __init__(self, place_symbol_event_id):
        super().__init__()
        self.place_symbol_event_id = place_symbol_event_id


class PlayerPlacedSymbolInGameEvent(InGameEvent):
    def __init__(self, player_id, position, confirmation, original_event_id=None):
        super().__init__()
        self.player_id = player_id
        self.position = position
        self.confirmation = confirmation
        self.original_event_id = original_event_id


class PlaceASymbolNetworkRequestEvent(Event):
    def __init__(self, game_id, event_id, position):
        super().__init__()
        self.game_id = game_id
        self.event_id = event_id
        self.position = position


class SymbolPlacedErroredEvent(InGameEvent):
    # This indicates that a chat message wasn't sucessfully processed
    # by the server and therefore it needs to be rolled back.
    def __init__(self, place_symbol_event_id):
        super().__init__()
        self.place_symbol_event_id = place_symbol_event_id
