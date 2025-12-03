from components.api import create_fade_in
from engine.api import (
    DisableUserInput,
    EnableUserInput,
    HideCursor,
    PlayMusic,
    PlaySound,
    Screen,
    ShowCursor,
    Timer,
)

from .ui import (
    create_background,
    create_clickable_area_1,
    create_clickable_area_2,
    create_clickable_area_3,
    create_clickable_area_4,
)


def on_click():
    pass


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = [
            create_background(),
            create_clickable_area_1(on_click),
            create_clickable_area_2(on_click),
            create_clickable_area_3(on_click),
            create_clickable_area_4(on_click),
            create_fade_in(),
        ]
        self.timers = [Timer(700, self.on_intro_finished)]

    def initialize(self):
        PlayMusic(
            "assets/sounds/ambient.ogg",
        ).execute()
        PlaySound(
            "assets/sounds/intro.ogg",
        ).execute()
        DisableUserInput().execute()
        HideCursor().execute()

    def on_intro_finished(self) -> None:
        EnableUserInput().execute()
        ShowCursor().execute()
