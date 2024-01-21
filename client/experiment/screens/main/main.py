import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

from client.engine.features.user_input.events import UserClickedEvent
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

        self.events = {UserClickedEvent: self.on_user_clicked}

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        logger.info(f"User clicked at {event.coordinates[0]}, {event.coordinates[1]}")
