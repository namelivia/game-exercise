from client.primitives.screen import Screen
from .ui import Background
from client.events import UserTypedEvent


class Options(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            # Avoid circular import
            pass
            return
