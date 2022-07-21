from client.primitives.screen import Screen
from .ui import EnterNameMessage, Background
from client.events import UserTypedEvent
from client.game.commands import PlaySound


class EnterName(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"name": ""}

        self.ui_elements = [
            Background(),
            EnterNameMessage(self.data["name"]),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed
        }

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            # Avoid circular import
            # TODO: Run a comand to set the name
            from client.commands import SetPlayerName
            from client.game.commands import BackToLobby

            SetPlayerName(self.client_state.profile, self.client_state.queue, self.data["name"]).execute()
            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            pass
        if event.key == "backspace":
            PlaySound(
                self.client_state.profile, self.client_state.queue, "erase"
            ).execute()
            self.data["name"] = self.data["name"][:-1]
            return
        else:
            PlaySound(
                self.client_state.profile, self.client_state.queue, "type"
            ).execute()
            self.data["name"] += event.key