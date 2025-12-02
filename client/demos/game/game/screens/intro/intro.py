from components.api import create_fade_in, create_fade_out
from engine.api import (
    AnimationFinishedEvent,
    DisableUserInput,
    EnableUserInput,
    HideCursor,
    PlayMusic,
    PlaySound,
    Screen,
    ScreenTransition,
    ShowCursor,
    Timer,
    UserTypedEvent,
)

from game.screens.lobby.lobby import Lobby

from .ui import create_background, create_coin_1, create_coin_2, create_title


class Intro(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_title(),
            create_fade_in(),
        ]

        self.timers = [
            Timer(1000, self.show_coin_1),
            Timer(1200, self.show_coin_2),
            Timer(3000, self.go_to_lobby),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
        }

    def initialize(self) -> None:
        PlayMusic(
            "assets/music/main_theme.mp3",
        ).execute()
        HideCursor().execute()
        DisableUserInput()

    # Actions
    def go_to_lobby(self) -> None:
        self.add_ui_element(create_fade_out())
        DisableUserInput().execute()

    def show_coin_1(self) -> None:
        PlaySound(
            "assets/sounds/user_connected.mp3",
        ).execute()
        ShowCursor().execute()
        EnableUserInput().execute()
        self.add_ui_element(create_coin_1())

    def show_coin_2(self) -> None:
        PlaySound(
            "assets/sounds/user_connected.mp3",
        ).execute()
        self.add_ui_element(create_coin_2())

    def go_to_next_screen(self):
        PlaySound("assets/sounds/select.mp3").execute()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            PlaySound("assets/sounds/select.mp3").execute()
            self.go_to_lobby()

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()
