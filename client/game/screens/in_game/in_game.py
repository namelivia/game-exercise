from client.primitives.screen import Screen
from .ui import (
    TurnIndicator,
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    Board,
    Instructions,
)
from client.game.events import (
    UserTypedEvent,  # This could be generic
    GameCreatedEvent,
    PlayerJoinedEvent,
    PlayerPlacedSymbolEvent
)


class InGame(Screen):
    def __init__(
        self,
        client_state,
        window,
        turn,
        board,
        events,
        game_id,
        name,
        player_1_id,
        player_2_id
    ):
        super().__init__(client_state, window)

        self.data = {
            "turn": turn,
            "board": board,
            "events": events,
            "game_id": game_id,
            "name": name,
            "player_1_id": player_1_id,
            "player_2_id": player_2_id

        }

        self.ui_elements = [
            TurnIndicator(self.data['turn']),
            GameIdIndicator(self.data['game_id']),
            GameNameIndicator(self.data['name']),
            Player1NameIndicator(self.data['player_1_id']),
            Player2NameIndicator(self.data['player_2_id']),
            Board(self.data['board']),
            Instructions(),
        ]

    def update(self, event):
        super().update()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                # Avoid circular import
                from client.game.commands import (
                    BackToLobby,
                    RequestPlaceASymbol
                )
                if event.key == "escape":
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                if event.key in "012345678":
                    RequestPlaceASymbol(
                        self.client_state.profile,
                        self.client_state.queue,
                        event.key
                    ).execute()
            if isinstance(event, GameCreatedEvent):
                print("Game created, do something play some music, update the internal state or something")
            if isinstance(event, PlayerJoinedEvent):
                print("Player joined, do something play some music, update the internal state or something")
            if isinstance(event, PlayerPlacedSymbolEvent):
                print("Player placed a symbol, do something play some music, update the internal state or something")
