from engine.api import Screen, ScreenTransition, UserTypedEvent

from .ui import create_background, create_options, create_welcome_message


class Lobby(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_welcome_message(),
            create_options(
                {
                    "1": "Create a new game",
                    "2": "Join an existing game",
                    "3": "Game list",
                    "4": "Options",
                    "5": "Set Name",
                    "6": "Credits",
                    "7": "Profiles",
                }
            ),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        key = event.key
        if key == "1":
            pass
        if key == "2":
            pass
        if key == "3":
            pass
        if key == "4":
            pass
        if key == "5":
            pass
        if key == "6":
            from game.screens.credits.credits import Credits

            ScreenTransition(Credits).execute()
        if key == "7":
            pass
