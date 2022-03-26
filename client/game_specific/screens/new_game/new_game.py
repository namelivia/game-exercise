from client.primitives.screen import Screen
from .ui import (
    NewGameMessage
)
from client.game_specific.events import UserTypedEvent  # This could be generic


class NewGame(Screen):

    def __init__(self, client_state, window):
        super().__init__(client_state, window)

        self.data = {
            "new_game_name": ""
        }

        self.ui_elements = [
            NewGameMessage(self.data['new_game_name']),
        ]

    def update(self, event):
        super().update()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        BackToLobby
                    )
                    BackToLobby(
                        self.client_state.profile,
                        self.client_state.queue
                    ).execute()
                    return
                if event.key == "return":
                    # Avoid circular import
                    from client.game_specific.commands import (
                        RequestGameCreation
                    )
                    RequestGameCreation(
                        self.client_state.profile,
                        self.client_state.queue,
                        self.data["new_game_name"]
                    ).execute()
                    return
                if event.key == "backspace":
                    self.data["new_game_name"] = self.data["new_game_name"][:-1]
                    return
                else:
                    self.data["new_game_name"] += event.key
