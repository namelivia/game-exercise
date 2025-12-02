from components.api import create_fade_in, create_fade_out
from engine.api import (
    AnimationFinishedEvent,
    DisableUserInput,
    EnableUserInput,
    PlaySound,
    Screen,
    ScreenTransition,
    TurnSoundOff,
    TurnSoundOn,
    UserTypedEvent,
)

from .ui import create_background, create_options, create_title


class Options(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_title(),
            create_options({"1": "Sound ON", "2": "Soud OFF"}),
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
        if event.key == "1":
            TurnSoundOn().execute()
            return
        if event.key == "2":
            TurnSoundOff().execute()
            return

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()
