import pygame
from .sprite import Sprite
from client.primitives.shape import Shape

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Text(Shape):
    def __init__(self, message, x, y, color=BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text_surface = font.render(self.message, True, self.color)
            window.blit(text_surface, dest=(self.x, self.y))

    def set_message(self, message):
        self.message = message


class Rectangle(Shape):
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.color = color

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            rectangle = pygame.Surface((self.width, self.height))
            rectangle.fill(self.color)
            rectangle.set_alpha(128)  # TODO: Alpha could be passed
            window.blit(rectangle, dest=(self.x, self.y))


class SmallText(Shape):
    def __init__(self, message, x, y, color=BLACK):
        super().__init__(x, y)
        self.message = message
        self.color = color

    def render(self, window):
        if window is not None:  # TODO: only if pygame
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            text_surface = font.render(self.message, True, self.color)
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
