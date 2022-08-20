from client.engine.primitives.screen import Screen
from .ui import GameListTitle, Games, Background, ErrorPopup, ErrorJoiningPopup
from client.engine.events import (
    UserTypedEvent,
    UpdateGameListEvent,
    ErrorGettingGameListEvent,
    ErrorJoiningGameEvent,
)


class GameList(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"games": []}

        self.ui_elements = [
            Background(),
            Games(self.data["games"]),
            GameListTitle(),
            ErrorPopup(),
            ErrorJoiningPopup(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            UpdateGameListEvent: self.on_game_list_updated,
            ErrorGettingGameListEvent: self.on_error_getting_game_list,
            ErrorJoiningGameEvent: self.on_error_joining_game,
        }

        from client.engine.commands import GetGameList

        GetGameList(self.client_state.profile, self.client_state.queue).execute()

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key in "012345678":
            from client.engine.commands import RequestJoiningAGame

            RequestJoiningAGame(
                self.client_state.profile,
                self.client_state.queue,
                self.data["games"][int(event.key)].id,
            ).execute()

    def on_game_list_updated(self, event):
        self.data["games"] = event.games

    def on_error_getting_game_list(self, event):
        self.ui_elements[3].show()

    def on_error_joining_game(self, event):
        self.ui_elements[4].show()
