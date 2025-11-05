import os

from engine.features.render.ui_element import UIElementRender
from engine.graphics.shapes import Animation
from engine.ui.ui import AnimationState, UIElement, UIElementLogic

from .loader import load_animation


def create_animation(json_file_path, x, y, fps):
    sprite_data = load_animation(json_file_path)
    json_file_dir = os.path.abspath(os.path.dirname(json_file_path))

    state = AnimationState(x, y, sprite_data.animations, fps)

    shape = Animation(
        os.path.join(json_file_dir, sprite_data.image),
        x,
        y,
        sprite_data.rows,
        sprite_data.columns,
    )
    render = UIElementRender(state, [shape])
    return UIElement(render, UIElementLogic(state))
