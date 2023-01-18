import pygame


class Music:
    @staticmethod
    def load(path):
        pygame.mixer.music.load(path)

    @staticmethod
    def play():
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()
