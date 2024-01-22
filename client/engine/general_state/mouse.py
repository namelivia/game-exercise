import pygame


class Mouse:
    def get(self) -> int:
        return pygame.mouse.get_pos()
