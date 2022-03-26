class Graphics():
    def __init__(self, uses_pygame):
        self.uses_pygame = uses_pygame
        if uses_pygame:
            import pygame
            self.window = pygame.display.set_mode((640, 480))
        else:
            self.window = None

    def render(self, screen):
        ui_elements = screen.get_ui_elements()
        import pygame
        if self.uses_pygame:
            self.window.fill((255, 255, 255))  # Clear the window (only pygame)
        [ui_element.render(self.window) for ui_element in ui_elements]  # Always
        if self.uses_pygame:
            pygame.display.update()  # Only pygame
