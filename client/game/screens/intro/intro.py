from client.engine.features.sound.commands import PlayMusic, PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, Coins, Title


class Intro(Screen):
    def __init__(self):
        super().__init__()

        self.ui_elements = [
            Background(),
            Coins(),
            Title(),
        ]

        client_state = ClientState()
        PlayMusic(
            client_state.queue,
            "client/game/music/main_theme.mp3",
        ).execute()

        self.timers = {
            10000: self.show_coins,
            30000: self.go_back_to_lobby,
        }

        self.events = {UserTypedEvent: self.on_user_typed}

    # Actions
    def go_back_to_lobby(self) -> None:
        from client.game.commands import BackToLobby

        client_state = ClientState()
        BackToLobby(client_state.queue).execute()

    def show_coins(self) -> None:
        client_state = ClientState()
        PlaySound(
            client_state.queue,
            "client/game/sounds/user_joined.mp3",
        ).execute()
        self.ui_elements[1].show()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import ToLobby

            client_state = ClientState()
            ToLobby(client_state.queue).execute()
