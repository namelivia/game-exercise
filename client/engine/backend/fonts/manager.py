import pygame


class FontManager:
    @staticmethod
    def get_default_font() -> str:
        return pygame.font.get_default_font()

    @staticmethod
    def get_font(font: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font, size)
