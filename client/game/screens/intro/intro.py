from client.primitives.screen import Screen
from client.game.sounds import UserJoinedSound
from client.game.music import MainThemeMusic
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

        self.sounds = [
            UserJoinedSound()
        ]

        MainThemeMusic().play()

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

        if (self.time == 10000):  # TODO: This sould be transformed in a command
            self.sounds[0].play()
            self.ui_elements[1].appear()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape" or event.key == "return":
                    # Avoid circular import
                    from client.game.commands import (
                        ToLobby
                    )
                    ToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
