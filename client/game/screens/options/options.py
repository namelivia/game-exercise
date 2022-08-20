from client.engine.primitives.screen import Screen
from .ui import Background, OptionsTitle, OptionList
from client.engine.events import UserTypedEvent


class Options(Screen):
    def __init__(self, client_state):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            OptionsTitle(),
            OptionList({"1": "Sound ON", "2": "Soud OFF"}),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event):
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "1":
            from client.engine.commands import TurnSoundOn

            TurnSoundOn(self.client_state.profile, self.client_state.queue).execute()
        if event.key == "2":
            from client.engine.commands import TurnSoundOff

            TurnSoundOff(self.client_state.profile, self.client_state.queue).execute()
