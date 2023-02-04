import pygame


class Clock:
    def tick(self) -> None:
        pass

    def get(self) -> int:
        return pygame.time.get_ticks()
