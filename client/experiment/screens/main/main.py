from typing import TYPE_CHECKING

from client.engine.primitives.screen import Screen

from .ui import Background

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class MainScreen(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
        ]
