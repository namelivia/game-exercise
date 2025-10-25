from typing import Any, Dict

from client.animation.images import ANIMATION, ANIMATION_OLD, BACKGROUND
from client.engine.animation_factory import create_animation
from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import UIElementState, create_ui_element


def create_background():
    return create_ui_element([Image(BACKGROUND, 0, 0)])


class AnimationSate(UIElementState):
    def __init__(self, x, y, frame):
        super().__init__(x, y)
        self.frame = frame


def create_debug_animation():
    return create_animation(ANIMATION, 50, 50)
