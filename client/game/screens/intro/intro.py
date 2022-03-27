from client.primitives.screen import Screen
from .ui import (
    Title,
    Background,
    Coins
)
from client.game.events import UserTypedEvent  # This could be generic


class Intro(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.ui_elements = [
            Background(),
            Coins(),
            Title(self.time),
        ]

    def update(self, event):
        super().update()

        # Time based triggers
        if (self.time > 30000):
            from client.game.commands import (
                BackToLobby
            )
            BackToLobby(
                self.client_state.profile,
                self.client_state.queue
            ).execute()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape" or event.key == "return":
                    # Avoid circular import
                    from client.game.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
