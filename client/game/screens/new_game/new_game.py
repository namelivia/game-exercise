from client.engine.primitives.screen import Screen
from .ui import NewGameMessage, Background, ErrorPopup
from client.events import UserTypedEvent, ErrorCreatingGameEvent
from client.game.commands import PlaySound


class NewGame(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"new_game_name": ""}

        self.ui_elements = [
            Background(),
            NewGameMessage(self.data["new_game_name"]),
            ErrorPopup()
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            ErrorCreatingGameEvent: self.on_error_creating_game,
        }

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            # Avoid circular import
            from client.commands import RequestGameCreation

            RequestGameCreation(
                self.client_state.profile,
                self.client_state.queue,
                self.data["new_game_name"],
            ).execute()
            return
        if event.key == "backspace":
            PlaySound(
                self.client_state.profile, self.client_state.queue, "erase"
            ).execute()
            self.data["new_game_name"] = self.data["new_game_name"][:-1]
            return
        else:
            PlaySound(
                self.client_state.profile, self.client_state.queue, "type"
            ).execute()
            self.data["new_game_name"] += event.key

    def on_error_creating_game(self, event):
        self.ui_elements[2].show()
