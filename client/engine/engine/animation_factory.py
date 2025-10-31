import json
import os
from dataclasses import dataclass, field
from typing import Dict, List

from engine.features.render.ui_element import UIElementRender
from engine.graphics.shapes import Animation
from engine.primitives.ui import AnimationState, UIElement, UIElementLogic


@dataclass
class SpriteSheetData:
    image: str
    rows: int
    columns: int
    animations: Dict[str, List[int]] = field(default_factory=dict)


def create_animation(json_file_path, x, y, fps):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    sprite_data = SpriteSheetData(**data)
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
