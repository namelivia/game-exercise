#from client.engine.features.game_management.commands import RequestJoiningAGame
#from client.engine.features.game_management.events import ErrorJoiningGameEvent
from engine.api import PlaySound, Screen, ScreenTransition, UserTypedEvent

from .ui import create_background, create_error_popup, create_game_id_input


class JoinGame(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"game_id": ""}

        self.ui_elements = [
            create_background(),
            create_error_popup(),
            create_game_id_input(self.data["game_id"]),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            # ErrorJoiningGameEvent: self.on_error_joining_game,
        }

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            return
        if event.key == "return":
            # RequestJoiningAGame(
            #    self.data["game_id"],
            # ).execute()
            return
        if event.key == "backspace":
            PlaySound(
                "assets/sounds/erase.mp3",
            ).execute()
            self.data["game_id"] = self.data["game_id"][:-1]
            return
        else:
            PlaySound(
                "assets/sounds/type.mp3",
            ).execute()
            self.data["game_id"] += event.key

    # def on_error_joining_game(self, event: ErrorJoiningGameEvent) -> None:
        # self.ui_elements[2].show()
