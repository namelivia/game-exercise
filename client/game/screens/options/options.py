from client.engine.features.sound.commands import TurnSoundOff, TurnSoundOn
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.general_state.client_state import ClientState
from client.engine.primitives.screen import Screen

from .ui import Background, OptionList, OptionsTitle


class Options(Screen):
    def __init__(self):
        super().__init__()

        self.ui_elements = [
            Background(),
            OptionsTitle(),
            OptionList({"1": "Sound ON", "2": "Soud OFF"}),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape":
            # Avoid circular import
            from client.game.commands import BackToLobby

            client_state = ClientState()
            BackToLobby(client_state.queue).execute()
            return
        if event.key == "1":
            client_state = ClientState()
            TurnSoundOn(client_state.queue).execute()
        if event.key == "2":
            client_state = ClientState()
            TurnSoundOff(client_state.queue).execute()
