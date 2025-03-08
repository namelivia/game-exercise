from client.engine.features.game_list.commands import GetGameList
from client.engine.features.game_list.events import (
    ErrorGettingGameListEvent,
    UpdateGameListEvent,
)
from client.engine.features.game_management.commands import RequestJoiningAGame
from client.engine.features.game_management.events import ErrorJoiningGameEvent
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, ErrorJoiningPopup, ErrorPopup, GameListTitle, Games


class GameList(Screen):
    def __init__(self) -> None:
        super().__init__()

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

        client_state = ClientState()
        GetGameList(client_state.queue).execute()

    def on_user_typed(self, event: "UserTypedEvent") -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            client_state = ClientState()
            BackToLobby(client_state.queue).execute()
            return
        if event.key in "012345678":
            client_state = ClientState()
            RequestJoiningAGame(
                client_state.queue,
                self.data["games"][int(event.key)].id,
            ).execute()

    def on_game_list_updated(self, event: "UpdateGameListEvent") -> None:
        self.data["games"] = event.games

    def on_error_getting_game_list(self, event: "ErrorGettingGameListEvent") -> None:
        self.ui_elements[3].show()

    def on_error_joining_game(self, event: "ErrorJoiningGameEvent") -> None:
        self.ui_elements[4].show()
