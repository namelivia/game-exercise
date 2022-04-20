from client.primitives.screen import Screen
from .ui import (
    WelcomeMessage,
    OptionList,
    Background,
)
from client.events import UserTypedEvent


class Lobby(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"name": client_state.profile.name}

        self.ui_elements = [
            Background(),
            WelcomeMessage(self.data["name"]),
            OptionList({"1": "Create a new game", "2": "Join an existing game"}),
        ]

    def update(self, event):
        super().update()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                # Avoid circular import
                # Could these be not just game specific but screen specific?
                from client.game.commands import NewGame, GoToJoinAGame
                from client.commands import QuitGame

                # These actions, some may update the data, others run commands, who knows
                key = event.key
                if key == "1":
                    NewGame(
                        self.client_state.profile, self.client_state.queue
                    ).execute()
                if key == "2":
                    GoToJoinAGame(
                        self.client_state.profile, self.client_state.queue
                    ).execute()
                if event.key == "escape":
                    QuitGame(
                        self.client_state.profile, self.client_state.queue
                    ).execute()
