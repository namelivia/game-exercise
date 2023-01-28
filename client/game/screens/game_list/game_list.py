from client.engine.primitives.screen import Screen
from .ui import GameListTitle, Games, Background, ErrorPopup, ErrorJoiningPopup
from client.engine.features.user_input.events import (
    UserTypedEvent,
)
from client.engine.features.game_list.events import (
    UpdateGameListEvent,
    ErrorGettingGameListEvent,
)
from client.engine.features.game_list.commands import GetGameList
from client.engine.features.game_management.commands import RequestJoiningAGame
from client.engine.features.game_management.events import (
    ErrorJoiningGameEvent,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class GameList(Screen):
    def __init__(self, client_state: "ClientState"):
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

        GetGameList(self.client_state.profile, self.client_state.queue).execute()

    def on_user_typed(self, event: "UserTypedEvent") -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key in "012345678":
            RequestJoiningAGame(
                self.client_state.profile,
                self.client_state.queue,
                self.data["games"][int(event.key)].id,
            ).execute()

    def on_game_list_updated(self, event: "UpdateGameListEvent") -> None:
        self.data["games"] = event.games

    def on_error_getting_game_list(self, event: "ErrorGettingGameListEvent") -> None:
        self.ui_elements[3].show()

    def on_error_joining_game(self, event: "ErrorJoiningGameEvent") -> None:
        self.ui_elements[4].show()
