from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.primitives.screen import Screen

from .ui import Background, OptionList, WelcomeMessage


class Lobby(Screen):
    def __init__(self) -> None:
        super().__init__()

        profile_what = ProfileWhat()
        self.data = {"name": profile_what.profile.name, "id": profile_what.profile.id}

        self.ui_elements = [
            Background(),
            WelcomeMessage(self.data["name"], self.data["id"]),
            OptionList(
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
        # Avoid circular import
        # Could these be not just game specific but screen specific?
        from client.engine.commands import PingTheServer, QuitGame
        from client.game.commands import (
            GoToCredits,
            GoToGameList,
            GoToJoinAGame,
            GoToOptions,
            GoToProfiles,
            GoToSetName,
            NewGame,
        )

        # These actions, some may update the data, others run commands, who knows
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
        if key == "p":
            PingTheServer().execute()
        if event.key == "escape":
            QuitGame().execute()
