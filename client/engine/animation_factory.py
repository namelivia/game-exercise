import json
import os
from dataclasses import dataclass, field
from typing import Dict, List

from client.engine.features.render.temp import UIElementRender
from client.engine.graphics.shapes import Animation
from client.engine.primitives.ui import AnimationState, UIElement, UIElementLogic


@dataclass
class SpriteSheetData:
    image: str
    rows: int
    columns: int
    animations: Dict[str, List[int]] = field(default_factory=dict)


# Animation factory!
# In order to create an animation, we need to open and parse
# the json file that describes it. And use that information
# to create the shape that will be rendered on the screen.
def create_animation(json_file_path, x, y):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    sprite_data = SpriteSheetData(**data)
    json_file_dir = os.path.abspath(os.path.dirname(json_file_path))

    state = AnimationState(x, y, sprite_data.animations)

    shape = Animation(
        os.path.join(json_file_dir, sprite_data.image),
        x,
        y,
        sprite_data.rows,
        sprite_data.columns,
    )
    render = UIElementRender(state, [shape])
    return UIElement(render, UIElementLogic(state))
