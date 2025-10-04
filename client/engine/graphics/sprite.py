import os
from re import sub
from typing import List

from client.engine.backend.foundational_wrapper import (
    FoundationalSprite,
    FoundationalWrapper,
)


class Sprite(FoundationalSprite):
    def _get_frames_path(self, folder: str) -> List[str]:
        path, _, files = next(os.walk(folder))
        files = [os.path.join(path, file) for file in files]
        files.sort(
            key=lambda f: int(sub(r"\D", "", f))
        )  # Sort filenames by the number included in it
        return files

    def _animation_length(self) -> int:
        return len(self.sprites)

    def __init__(self, folder: str, x: int, y: int, initial_frame: int):
        super().__init__()
        self.sprites = [
            FoundationalWrapper.load_image(frame)
            for frame in self._get_frames_path(folder)
        ]
        self.current_sprite = initial_frame % self._animation_length()
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        self.current_sprite = (self.current_sprite + 1) % self._animation_length()
        self.image = self.sprites[self.current_sprite]

    def set_x(self, x: int) -> None:
        if self.rect is not None:
            self.rect.x = x

    def set_y(self, y: int) -> None:
        if self.rect is not None:
            self.rect.y = y

    def get_x(self) -> int:
        return self.rect.x

    def get_y(self) -> int:
        return self.rect.y

    def get_width(self) -> int:
        return self.rect.width

    def get_height(self) -> int:
        return self.rect.height
