from client.primitives.screen import Screen
from .ui import GameListTitle, Background
from client.events import UserTypedEvent


# TODO: This is currently blocked because the server only answers with Game Messages
class GameList(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            GameListTitle(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "return":
            return
