from client.primitives.screen import Screen
from .ui import GameListTitle, Games, Background
from client.events import UserTypedEvent, UpdateGameListEvent


class GameList(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {
            "games": []
        }

        self.ui_elements = [
            Background(),
            Games(self.data["games"]),
            GameListTitle(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            UpdateGameListEvent: self.on_game_list_updated,
        }

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            from client.commands import GetGameList
            GetGameList(self.client_state.profile, self.client_state.queue).execute()
            return

    def on_game_list_updated(self, event):
        self.data["games"] = event.games
