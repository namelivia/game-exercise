import pygame


class Text():
    def __init__(self, message, x, y):
        self.message = message
        self.x = x
        self.y = y

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text_surface = font.render(self.message, True, (0, 0, 0))
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message):
        self.message = message

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class SmallText():
    def __init__(self, message, x, y):
        self.message = message
        self.x = x
        self.y = y

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            text_surface = font.render(self.message, True, (0, 0, 0))
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message):
        self.message = message

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
