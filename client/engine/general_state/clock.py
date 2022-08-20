import pygame


class Clock:
    def tick(self):
        pass

    def get(self):
        # TODO: Waaaait,this is pygame dependent
        return pygame.time.get_ticks()
