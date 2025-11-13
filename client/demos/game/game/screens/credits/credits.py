from engine.api import Screen, ScreenTransition, UserTypedEvent

from .ui import create_background, create_credits


class Credits(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_credits(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
