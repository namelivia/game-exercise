import pygame
from .sprite import Sprite
from client.primitives.shape import Shape


class Text(Shape):
    def __init__(self, message, x, y):
        super().__init__(x, y)
        self.message = message

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text_surface = font.render(self.message, True, (0, 0, 0))
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message):
        self.message = message


class SmallText(Shape):
    def __init__(self, message, x, y):
        super().__init__(x, y)
        self.message = message

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            text_surface = font.render(self.message, True, (0, 0, 0))
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message):
        self.message = message


class Image(Shape):
    def __init__(self, path, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load(path)

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            window.blit(self.image, dest=(self.x, self.y))


class Animation(Shape):
    def __init__(self, folder, x, y, initial_frame=0):
        super().__init__(x, y)
        self.sprite_group = pygame.sprite.Group()
        self.animation = Sprite(folder, x, y, initial_frame)
        self.sprite_group.add(self.animation)

    def set_x(self, x):
        super().set_x(x)
        self.animation.set_x(x)

    def set_y(self, y):
        super().set_y(y)
        self.animation.set_y(y)

    def update(self):
        self.sprite_group.update()  # Calls update on every sprite on the group

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            self.sprite_group.draw(window)
