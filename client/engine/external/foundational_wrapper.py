from typing import Any, List, Tuple

import pygame


class FoundationalSprite(pygame.sprite.Sprite):
    pass


class FoundationalColor(pygame.Color):
    pass


class FoundationalSurface(pygame.Surface):
    pass


class FoundationalWrapper:
    K_RETURN = pygame.K_RETURN
    K_ESCAPE = pygame.K_ESCAPE
    K_BACKSPACE = pygame.K_BACKSPACE
    KEYDOWN = pygame.KEYDOWN
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

    @staticmethod
    def get_event() -> List[pygame.event.Event]:
        return pygame.event.get()

    @staticmethod
    def quit() -> None:
        pygame.quit()
        return None

    @staticmethod
    def update_display() -> None:
        pygame.display.update()
        return None

    @staticmethod
    def get_new_window(width: int, height: int) -> pygame.Surface:
        return pygame.display.set_mode((width, height))

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

    @staticmethod
    def get_clock_ticks() -> int:
        return int(pygame.time.get_ticks())

    @staticmethod
    def get_mouse_position() -> Tuple[int, int]:
        return pygame.mouse.get_pos()

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        return pygame.image.load(path)

    # TODO: I had to add Any here as I could not find a way to type hint this
    @staticmethod
    def sprite_group() -> Any:
        return pygame.sprite.Group()

    @staticmethod
    def get_default_font() -> str:
        return pygame.font.get_default_font()

    @staticmethod
    def get_font(font: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(font, size)
