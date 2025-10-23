from client.animation.images import ANIMATION, BACKGROUND
from client.engine.graphics.shapes import Animation, Image
from client.engine.primitives.ui import create_ui_element


def create_background():
    return create_ui_element([Image(BACKGROUND, 0, 0)])


def create_animation():
    return create_ui_element([Animation(ANIMATION, 100, 100, 3, 3)])
