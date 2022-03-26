import pygame


class Text():
    def __init__(self, message, x, y):
        self.text_already_printed = False
        self.message = message
        self.x = x
        self.y = y

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text_surface = font.render(self.message, True, (0, 0, 0))
            window.blit(text_surface, dest=(self.x, self.y))
        if not self.text_already_printed:  # Text only mode
            print(self.message)
            self.text_already_printed = True

    def set_message(self, message):
        self.message = message
        self.text_already_printed = False  # If the text changes needs to be rewritten

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
