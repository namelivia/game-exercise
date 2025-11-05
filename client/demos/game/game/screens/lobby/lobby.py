from engine.api import Screen, UserTypedEvent

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
        from game.commands import (
            GoToCredits,
            GoToGameList,
            GoToJoinAGame,
            GoToOptions,
            GoToProfiles,
            GoToSetName,
            NewGame,
        )

        key = event.key
        if key == "1":
            NewGame().execute()
        if key == "2":
            GoToJoinAGame().execute()
        if key == "3":
            GoToGameList().execute()
        if key == "4":
            GoToOptions().execute()
        if key == "5":
            GoToSetName().execute()
        if key == "6":
            GoToCredits().execute()
        if key == "7":
            GoToProfiles().execute()
