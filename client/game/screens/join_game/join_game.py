from typing import TYPE_CHECKING

from client.engine.features.game_management.commands import RequestJoiningAGame
from client.engine.features.game_management.events import ErrorJoiningGameEvent
from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen

from .ui import Background, ErrorPopup, GameIdMessage

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class JoinGame(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

        self.data = {"game_id": ""}

        self.ui_elements = [
            Background(),
            GameIdMessage(self.data["game_id"]),
            ErrorPopup(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            ErrorJoiningGameEvent: self.on_error_joining_game,
        }

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            RequestJoiningAGame(
                self.client_state.profile,
                self.client_state.queue,
                self.data["game_id"],
            ).execute()
            return
        if event.key == "backspace":
            PlaySound(
                self.client_state.profile,
                self.client_state.queue,
                "client/game/sounds/erase.mp3",
            ).execute()
            self.data["game_id"] = self.data["game_id"][:-1]
            return
        else:
            PlaySound(
                self.client_state.profile,
                self.client_state.queue,
                "client/game/sounds/type.mp3",
            ).execute()
            self.data["game_id"] += event.key

    def on_error_joining_game(self, event: ErrorJoiningGameEvent) -> None:
        self.ui_elements[2].show()
