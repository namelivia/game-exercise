import json
import os
from dataclasses import dataclass, field
from typing import Dict, List

from client.engine.graphics.shapes import Animation


@dataclass
class SpriteSheetData:
    image: str
    rows: int
    columns: int
    animations: Dict[str, List[int]] = field(default_factory=dict)


class AnimationState:
    def __init__(self, animations):
        self.playing = False
        self.animations = animations
        self.current_animation = list(self.animations.keys())[0]
        self.index = 0

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def current_frame(self):
        return self.animations[self.current_animation][self.index]

    def get_animations(self):
        return list(self.animations.keys())

    def set_animation(self, new_animation):
        self.current_animation = new_animation
        self.index = 0

    def update(self):
        if self.playing:
            animation_keys = self.animations[self.current_animation]
            self.index = (self.index + 1) % len(animation_keys)


# Animation factory!
# In order to create an animation, we need to open and parse
# the json file that describes it. And use that information
# to create the shape that will be rendered on the screen.
def create_animation(json_file_path, x, y):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    sprite_data = SpriteSheetData(**data)
    json_file_dir = os.path.abspath(os.path.dirname(json_file_path))

    # We need the shape
    shape = Animation(
        os.path.join(json_file_dir, sprite_data.image),
        x,
        y,
        sprite_data.rows,
        sprite_data.columns,
    )

    # But we also need the internal animation state
    # that will hold things like, if it is playing
    # if it is stopped, or what animation is playing
    state = AnimationState(sprite_data.animations)

    # There should be some functions to start playing,
    # stop, go to next frame or change the animation.
