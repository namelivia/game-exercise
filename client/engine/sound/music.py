import pygame


class Music:
    @staticmethod
    def load(path: str) -> None:
        pygame.mixer.music.load(path)

    @staticmethod
    def play() -> None:
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop() -> None:
        pygame.mixer.music.stop()
