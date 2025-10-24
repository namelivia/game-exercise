import logging

logger = logging.getLogger(__name__)

from client.engine.primitives.screen import Screen

from .ui import create_background, create_debug_animation


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = [
            create_background(),
            create_debug_animation(),
        ]
        self.events = {}
