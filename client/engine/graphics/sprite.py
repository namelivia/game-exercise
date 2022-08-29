import os
import pygame
from re import sub


class Sprite(pygame.sprite.Sprite):
    def _get_frames_path(self, folder):
        path, _, files = next(os.walk(folder))
        files = [os.path.join(path, file) for file in files]
        files.sort(
            key=lambda f: int(sub(r"\D", "", f))
        )  # Sort filenames by the number included in it
        return files

    def _animation_length(self):
        return len(self.sprites)

    def __init__(self, folder, x, y, initial_frame):
        super().__init__()
        self.sprites = [
            pygame.image.load(frame) for frame in self._get_frames_path(folder)
        ]
        self.current_sprite = initial_frame % self._animation_length()
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.current_sprite = (self.current_sprite + 1) % self._animation_length()
        self.image = self.sprites[self.current_sprite]

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y
