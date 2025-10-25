from typing import Any, Dict

from client.animation.images import ANIMATION, BACKGROUND
from client.engine.animation_factory import create_animation
from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import create_ui_element


def create_background():
    return create_ui_element([Image(BACKGROUND, 0, 0)])


def create_debug_animation():
    return create_animation(ANIMATION, 50, 50, 2)
