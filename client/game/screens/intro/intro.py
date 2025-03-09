from client.engine.features.sound.commands import PlayMusic, PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen

from .ui import Background, Coins, Title


class Intro(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            Background(),
            Coins(),
            Title(),
        ]

        PlayMusic(
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

        BackToLobby().execute()

    def show_coins(self) -> None:
        PlaySound(
            "client/game/sounds/user_joined.mp3",
        ).execute()
        self.ui_elements[1].show()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            # Avoid circular import
            from client.game.commands import ToLobby

            ToLobby().execute()
