from components.api import create_fade_in, create_fade_out

# from client.engine.features.game_management.commands import RequestJoiningAGame
# from client.engine.features.game_management.events import ErrorJoiningGameEvent
from engine.api import (
    AnimationFinishedEvent,
    DisableUserInput,
    EnableUserInput,
    PlaySound,
    Screen,
    ScreenTransition,
    UserTypedEvent,
)

from .ui import create_background, create_error_popup, create_game_id_input


class JoinGame(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"game_id": ""}

        self.ui_elements = [
            create_background(),
            create_error_popup(),
            create_game_id_input(self.data["game_id"]),
            create_fade_in(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
            # ErrorJoiningGameEvent: self.on_error_joining_game,
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

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()

    # def on_error_joining_game(self, event: ErrorJoiningGameEvent) -> None:
    # self.ui_elements[2].show()
