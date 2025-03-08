from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, CreditsUI


class Credits(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            Background(),
            CreditsUI(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import BackToLobby

            client_state = ClientState()
            BackToLobby(client_state.queue).execute()
