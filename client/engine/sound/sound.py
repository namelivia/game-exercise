import pygame


class Sound:
    @staticmethod
    def play(path: str) -> None:
        pygame.mixer.Sound.play(pygame.mixer.Sound(path))
