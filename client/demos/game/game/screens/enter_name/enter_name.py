from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen

from .ui import Background, EnterNameMessage


class EnterName(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"name": ""}

        self.ui_elements = [
            Background(),
            EnterNameMessage(self.data["name"]),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby().execute()
            return
        if event.key == "return":
            # Avoid circular import
            from client.engine.commands import SetPlayerName
            from client.game.commands import BackToLobby

            SetPlayerName(self.data["name"]).execute()
            BackToLobby().execute()
            pass
        if event.key == "backspace":
            PlaySound(
                "client/game/sounds/erase.mp3",
            ).execute()
            self.data["name"] = self.data["name"][:-1]
            return
        else:
            PlaySound(
                "client/game/sounds/type.mp3",
            ).execute()
            self.data["name"] += event.key
