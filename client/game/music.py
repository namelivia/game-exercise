import pygame


class MainThemeMusic:
    def __init__(self):
        self.sound = pygame.mixer.music.load("client/game/music/main_theme.mp3")

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()
