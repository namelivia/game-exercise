from client.engine.primitives.screen import Screen
from .ui import Background, OptionsTitle, OptionList
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.features.sound.commands import TurnSoundOn, TurnSoundOff
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class Options(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

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

            BackToLobby(self.client_state.profile, self.client_state.queue).execute()
            return
        if event.key == "1":
            TurnSoundOn(self.client_state.profile, self.client_state.queue).execute()
        if event.key == "2":
            TurnSoundOff(self.client_state.profile, self.client_state.queue).execute()
