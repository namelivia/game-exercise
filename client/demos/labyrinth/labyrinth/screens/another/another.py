from components.api import create_fade_in
from engine.api import (
    DisableUserInput,
    EnableUserInput,
    HideCursor,
    PlaySound,
    Screen,
    ShowCursor,
    Timer,
)
from labyrinth.ui_loader import load_ui


class AnotherScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = load_ui("labyrinth/screens/main/ui.json")
        self.timers = [Timer(700, self.on_intro_finished)]

    def initialize(self):
        PlaySound(
            "assets/sounds/intro.ogg",
        ).execute()
        DisableUserInput().execute()
        HideCursor().execute()

    def on_intro_finished(self) -> None:
        EnableUserInput().execute()
        ShowCursor().execute()
