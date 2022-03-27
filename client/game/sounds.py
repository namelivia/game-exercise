import pygame


class UserJoinedSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/user_connected.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)
