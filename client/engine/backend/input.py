from typing import List, Tuple

import pygame


class InputBackend:
    K_RETURN = pygame.K_RETURN
    K_ESCAPE = pygame.K_ESCAPE
    K_BACKSPACE = pygame.K_BACKSPACE
    KEYDOWN = pygame.KEYDOWN
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

    @staticmethod
    def get_event() -> List[pygame.event.Event]:
        return pygame.event.get()

    @staticmethod
    def get_mouse_position() -> Tuple[int, int]:
        return pygame.mouse.get_pos()
