import pygame

from ..constants import GRAPHICS


class PygameFontManager:
    def get_default_font(self) -> str:
        return "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"

    def get_font(self, font: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font, size)


class FreeTypeFontManager:
    pass  # TODO


class FontManager:

    @staticmethod
    def get():
        if GRAPHICS == "NATIVE":
            return PygameFontManager()
        else:
            return FreeTypeFontManager()
