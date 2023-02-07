from typing import TYPE_CHECKING

from client.engine.features.sound.commands import PlayMusic, PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen

from .ui import Background, Coins, Title

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class Intro(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            Coins(),
            Title(),
        ]

        PlayMusic(
            self.client_state.profile, self.client_state.queue, "main_theme"
        ).execute()

        self.timers = {
            10000: self.show_coins,
            30000: self.go_back_to_lobby,
        }

        self.events = {UserTypedEvent: self.on_user_typed}

    # Actions
    def go_back_to_lobby(self) -> None:
        from client.game.commands import BackToLobby

        BackToLobby(self.client_state.profile, self.client_state.queue).execute()

    def show_coins(self) -> None:
        PlaySound(
            self.client_state.profile, self.client_state.queue, "user_joined"
        ).execute()
        self.ui_elements[1].show()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import ToLobby

            ToLobby(self.client_state.profile, self.client_state.queue).execute()
