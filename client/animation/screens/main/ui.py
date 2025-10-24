from typing import Any, Dict

from client.animation.images import ANIMATION, ANIMATION_OLD, BACKGROUND
from client.engine.animation_factory import create_animation
from client.engine.graphics.shapes import Animation, Image
from client.engine.primitives.ui import (
    UIElementLogic,
    UIElementState,
    create_ui_element,
)


def create_background():
    return create_ui_element([Image(BACKGROUND, 0, 0)])


class AnimationLogic(UIElementLogic):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        inverse_speed = 8  # The higher the slower
        offset = 300
        self.state.set_x(
            int((time / inverse_speed) % (640 + offset) - offset)
        )  # Not supersure about this


class AnimationSate(UIElementState):
    def __init__(self, x, y, frame):
        super().__init__(x, y)
        self.frame = frame


def create_debug_animation():
    create_animation(ANIMATION, 0, 0)
    state = AnimationSate(20, 10, 0)
    return create_ui_element(
        [Animation(ANIMATION_OLD, 0, 0, 3, 3)], state, AnimationLogic(state)
    )
