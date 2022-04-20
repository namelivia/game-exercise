from client.primitives.screen import Screen
from .ui import GameIdMessage, Background
from client.events import UserTypedEvent
from client.game.events import PlaySoundEvent  # This could be generic


class JoinGame(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"game_id": ""}

        self.ui_elements = [
            Background(),
            GameIdMessage(self.data["game_id"]),
        ]

    def update(self, event):
        super().update()

        # Event based triggers
        if event is not None:
            if isinstance(event, UserTypedEvent):
                if event.key == "escape":
                    # Avoid circular import
                    from client.game.commands import BackToLobby

                    BackToLobby(
                        self.client_state.profile, self.client_state.queue
                    ).execute()
                    return
                if event.key == "return":
                    # Avoid circular import
                    from client.commands import RequestJoiningAGame

                    RequestJoiningAGame(
                        self.client_state.profile,
                        self.client_state.queue,
                        self.data["game_id"],
                    ).execute()
                    return
                if event.key == "backspace":
                    self.client_state.queue.put(PlaySoundEvent("erase"))
                    self.data["game_id"] = self.data["game_id"][:-1]
                    return
                else:
                    # TODO: Should this be a command instead of pushing directly to the queue?
                    self.client_state.queue.put(PlaySoundEvent("type"))
                    self.data["game_id"] += event.key
