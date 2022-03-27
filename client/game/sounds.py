import pygame


class UserJoinedSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/user_connected.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class BackSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/back.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class SelectSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/select.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class StartGameSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/start_game.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class TypeSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/type.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class EraseSound():
    def __init__(self):
        self.sound = pygame.mixer.Sound("client/game/sounds/erase.mp3")

    def play(self):
        pygame.mixer.Sound.play(self.sound)
