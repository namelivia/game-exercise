import pygame


class Clock:
    def tick(self) -> None:
        pass

    def get(self) -> int:
        # TODO: Waaaait,this is pygame dependent
        return pygame.time.get_ticks()
