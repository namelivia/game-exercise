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

from .ui import create_background, create_credits


class Credits(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [create_background(), create_credits(), create_fade_in()]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
        }

    def initialize(self):
        DisableUserInput().execute()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            PlaySound("assets/sounds/back.mp3").execute()
            self.add_ui_element(create_fade_out())
            DisableUserInput().execute()
            return

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()
