import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

from client.engine.features.user_input.events import UserClickedEvent
from client.engine.primitives.screen import Screen

from .ui import Background, Lion, LionHighlight

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class MainScreen(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

        self.ui_elements = [
            Background(),
            LionHighlight(),
            Lion(),
        ]

        self.events = {UserClickedEvent: self.on_user_clicked}

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        if self.ui_elements[2].mouse_over:
            logger.info("Clicked on lion!")
