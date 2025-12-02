# from client.engine.features.game_management.events import ErrorCreatingGameEvent
from components.api import create_fade_in, create_fade_out
from engine.api import (
    AnimationFinishedEvent,
    DisableUserInput,
    EnableUserInput,
    PlaySound,
    Screen,
    ScreenTransition,
    UserTypedEvent,
)

from .ui import create_background, create_error_popup, create_new_game_name_input


class CreateGame(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"new_game_name": ""}

        self.ui_elements = [
            create_background(),
            create_error_popup(),
            create_new_game_name_input(self.data["new_game_name"]),
            create_fade_in(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
            # ErrorCreatingGameEvent: self.on_error_creating_game,
        }

    def initialize(self) -> None:
        DisableUserInput().execute()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            self.add_ui_element(create_fade_out())
            DisableUserInput().execute()
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
    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()
