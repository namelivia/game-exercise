import logging

logger = logging.getLogger(__name__)

from client.animation.images import ANIMATION, BACKGROUND
from client.engine.animation_factory import create_animation
from client.engine.graphics.shapes import Image
from client.engine.primitives.screen import Screen
from client.engine.primitives.ui import create_ui_element


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = [
            create_ui_element([Image(BACKGROUND, 0, 0)]),
            create_animation(ANIMATION, 50, 50, 2),
        ]
        self.events = {}
