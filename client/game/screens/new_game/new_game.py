from client.primitives.screen import Screen
from .ui import NewGameMessage, Background
from client.events import UserTypedEvent
from client.game.events import PlaySoundEvent  # This could be generic


class NewGame(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.data = {"new_game_name": ""}

        self.ui_elements = [
            Background(),
            NewGameMessage(self.data["new_game_name"]),
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
                    from client.commands import RequestGameCreation

                    RequestGameCreation(
                        self.client_state.profile,
                        self.client_state.queue,
                        self.data["new_game_name"],
                    ).execute()
                    return
                if event.key == "backspace":
                    self.client_state.queue.put(PlaySoundEvent("erase"))
                    self.data["new_game_name"] = self.data["new_game_name"][:-1]
                    return
                else:
                    # TODO: Should this be a command instead of pushing directly to the queue?
                    self.client_state.queue.put(PlaySoundEvent("type"))
                    self.data["new_game_name"] += event.key
