import pygame


class SoundBackend:
    @staticmethod
    def init() -> None:
        pygame.mixer.init()
        return None

    @staticmethod
    def play_sound(path: str) -> None:
        pygame.mixer.Sound.play(pygame.mixer.Sound(path))
        return None

    @staticmethod
    def load_music(path: str) -> None:
        pygame.mixer.music.load(path)
        return None

    @staticmethod
    def play_music() -> None:
        pygame.mixer.music.play(-1)
        return None

    @staticmethod
    def stop_music() -> None:
        pygame.mixer.music.stop()
        return None
