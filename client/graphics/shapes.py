import pygame


class Text():
    def __init__(self, message, x, y):
        self.message = message
        self.x = x
        self.y = y

    def render(self, window):
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        text_surface = font.render(self.message, True, (0, 0, 0))
        window.blit(text_surface, dest=(self.x, self.y))
