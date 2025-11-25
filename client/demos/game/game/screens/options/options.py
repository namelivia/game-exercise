from engine.api import (
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
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
        if event.key == "1":
            TurnSoundOn().execute()
        if event.key == "2":
            TurnSoundOff().execute()
