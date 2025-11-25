# from client.engine.features.game_management.events import ErrorCreatingGameEvent

from engine.api import PlaySound, Screen, ScreenTransition, UserTypedEvent

from .ui import create_background, create_error_popup, create_new_game_name_input


class CreateGame(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"new_game_name": ""}

        self.ui_elements = [
            create_background(),
            create_error_popup(),
            create_new_game_name_input(self.data["new_game_name"]),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            # ErrorCreatingGameEvent: self.on_error_creating_game,
        }

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            return
        if event.key == "return":
            # RequestGameCreation(
            #    self.data["new_game_name"],
            # ).execute()
            return
        if event.key == "backspace":
            PlaySound(
                "assets/sounds/erase.mp3",
            ).execute()
            self.data["new_game_name"] = self.data["new_game_name"][:-1]
            return
        else:
            PlaySound(
                "assets/sounds/type.mp3",
            ).execute()
            self.data["new_game_name"] += event.key

    # def on_error_creating_game(self, event: ErrorCreatingGameEvent) -> None:
    # self.ui_elements[2].show()
