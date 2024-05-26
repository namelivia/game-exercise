import pygame


class FoundationalSprite(pygame.sprite.Sprite):
    pass


class FoundationalWrapper:
    K_RETURN = pygame.K_RETURN
    K_ESCAPE = pygame.K_ESCAPE
    K_BACKSPACE = pygame.K_BACKSPACE
    KEYDOWN = pygame.KEYDOWN
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

    @staticmethod
    def get_event():
        return pygame.event.get()

    @staticmethod
    def quit():
        pygame.quit()
        return None

    @staticmethod
    def update_display():
        pygame.display.update()
        return None

    @staticmethod
    def get_new_window(width: int, height: int):
        return pygame.display.set_mode((width, height))

    @staticmethod
    def play_sound(path: str):
        pygame.mixer.Sound.play(pygame.mixer.Sound(path))
        return None

    @staticmethod
    def load_music():
        pygame.mixer.music.load(path)
        return None

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)
        return None

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()
        return None

    @staticmethod
    def get_clock_ticks():
        return int(pygame.time.get_ticks())

    @staticmethod
    def get_mouse_position():
        return pygame.mouse.get_pos()

    @staticmethod
    def load_image(path: str):
        return pygame.image.load(path)
