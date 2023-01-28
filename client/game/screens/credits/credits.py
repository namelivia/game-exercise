from client.engine.primitives.screen import Screen
from .ui import CreditsUI, Background
from client.engine.features.user_input.events import UserTypedEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class Credits(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            CreditsUI(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
