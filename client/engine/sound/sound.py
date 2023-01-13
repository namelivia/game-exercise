import pygame


class Sound:
    @staticmethod
    def play(path):
        pygame.mixer.Sound.play(pygame.mixer.Sound(path))
