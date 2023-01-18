from client.engine.primitives.screen import Screen
from .ui import (
    WelcomeMessage,
    OptionList,
    Background,
)
from client.engine.features.user_input.events import UserTypedEvent


class Lobby(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"name": client_state.profile.name, "id": client_state.profile.id}

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

    def on_user_typed(self, event):
        # Avoid circular import
        # Could these be not just game specific but screen specific?
        from client.game.commands import (
            NewGame,
            GoToJoinAGame,
            GoToOptions,
            GoToGameList,
            GoToCredits,
            GoToSetName,
            GoToProfiles,
        )
        from client.engine.commands import QuitGame, PingTheServer

        # These actions, some may update the data, others run commands, who knows
        key = event.key
        if key == "1":
            NewGame(self.client_state.profile, self.client_state.queue).execute()
        if key == "2":
            GoToJoinAGame(self.client_state.profile, self.client_state.queue).execute()
        if key == "3":
            GoToGameList(self.client_state.profile, self.client_state.queue).execute()
        if key == "4":
            GoToOptions(self.client_state.profile, self.client_state.queue).execute()
        if key == "5":
            GoToSetName(self.client_state.profile, self.client_state.queue).execute()
        if key == "6":
            GoToCredits(self.client_state.profile, self.client_state.queue).execute()
        if key == "7":
            GoToProfiles(self.client_state.profile, self.client_state.queue).execute()
        if key == "p":
            PingTheServer(self.client_state.profile, self.client_state.queue).execute()
        if event.key == "escape":
            QuitGame(self.client_state.profile, self.client_state.queue).execute()
