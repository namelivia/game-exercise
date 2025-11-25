from engine.api import PlaySound, Screen, ScreenTransition, UserTypedEvent

from game.state import State

from .ui import create_background, create_name_input


class EnterName(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"name": ""}

        self.ui_elements = [
            create_background(),
            create_name_input(self.data["name"]),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            return
        if event.key == "return":
            PlaySound("assets/sounds/select.mp3").execute()
            State().set_player_name(self.data["name"])
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            return
        if event.key == "backspace":
            PlaySound(
                "assets/sounds/erase.mp3",
            ).execute()
            self.data["name"] = self.data["name"][:-1]
            return
        else:
            PlaySound(
                "assets/sounds/type.mp3",
            ).execute()
            self.data["name"] += event.key
