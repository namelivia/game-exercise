import pygame


class Backend:
    @staticmethod
    def quit() -> None:
        pygame.quit()
        return None

    @staticmethod
    def init() -> None:
        pygame.init()
        return None
