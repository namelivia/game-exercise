from client.primitives.screen import Screen
from .ui import (
    GameIdIndicator,
    GameNameIndicator,
    Player1NameIndicator,
    Player2NameIndicator,
    Instructions,
    Background,
)
from client.events import UserTypedEvent
from client.events import GameCreatedEvent, PlayerJoinedEvent, PlayerPlacedSymbolEvent


class InGame(Screen):
    def __init__(self, client_state, events, game_id, name, players):
        super().__init__(client_state)

        self.data = {
            "events": events,
            "game_id": game_id,
            "name": name,
            "players": players,
        }

        self.ui_elements = [
            Background(),
            GameIdIndicator(self.data["game_id"]),
            GameNameIndicator(self.data["name"]),
            Player1NameIndicator(self.data["players"][0]),
            Player2NameIndicator(None),
            Instructions(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            GameCreatedEvent: self.on_game_created,
            PlayerJoinedEvent: self.on_player_joined,
            PlayerPlacedSymbolEvent: self.on_player_placed_symbol,
        }

    def on_user_typed(self, event):
        # Avoid circular import
        from client.game.commands import BackToLobby, RequestPlaceASymbol

        if event.key == "escape":
            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
        if event.key in "012345678":
            RequestPlaceASymbol(
                self.client_state.profile, self.client_state.queue, event.key
            ).execute()

    def on_game_created(self, event):
        print(
            "Game created, do something play some music, update the internal state or something"
        )

    def on_player_joined(self, event):
        print(
            "Player Joined, do something play some music, update the internal state or something"
        )
        # self.data.player_2_id = event.player_id

    def on_player_placed_symbol(self, event):
        print(
            "Player placed a symbol, do something play some music, update the internal state or something"
        )
