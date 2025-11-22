import json

from .spritesheet import SpriteSheetData


def load_animation(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    return SpriteSheetData(**data)
