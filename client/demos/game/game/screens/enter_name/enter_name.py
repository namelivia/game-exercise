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

from game.state import State

from .ui import create_background, create_name_input


class EnterName(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"name": ""}

        self.ui_elements = [
            create_background(),
            create_name_input(self.data["name"]),
            create_fade_in(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
        }

    def initialize(self):
        DisableUserInput().execute()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            self.add_ui_element(create_fade_out())
            DisableUserInput().execute()
            return
        if event.key == "return":
            PlaySound("assets/sounds/select.mp3").execute()
            State().set_player_name(self.data["name"])
            self.add_ui_element(create_fade_out())
            DisableUserInput().execute()
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

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()
