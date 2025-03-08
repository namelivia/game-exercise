from client.engine.features.game_management.commands import RequestGameCreation
from client.engine.features.game_management.events import ErrorCreatingGameEvent
from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, ErrorPopup, NewGameMessage


class NewGame(Screen):
    def __init__(self):
        super().__init__()

        self.data = {"new_game_name": ""}

        self.ui_elements = [
            Background(),
            NewGameMessage(self.data["new_game_name"]),
            ErrorPopup(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            ErrorCreatingGameEvent: self.on_error_creating_game,
        }

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            client_state = ClientState()
            BackToLobby(client_state.queue).execute()
            return
        if event.key == "return":
            client_state = ClientState()
            RequestGameCreation(
                client_state.queue,
                self.data["new_game_name"],
            ).execute()
            return
        if event.key == "backspace":
            client_state = ClientState()
            PlaySound(
                client_state.queue,
                "client/game/sounds/erase.mp3",
            ).execute()
            self.data["new_game_name"] = self.data["new_game_name"][:-1]
            return
        else:
            client_state = ClientState()
            PlaySound(
                client_state.queue,
                "client/game/sounds/type.mp3",
            ).execute()
            self.data["new_game_name"] += event.key

    def on_error_creating_game(self, event: ErrorCreatingGameEvent) -> None:
        self.ui_elements[2].show()
