class Graphics():
    def __init__(self, uses_pygame):
        self.uses_pygame = uses_pygame
        self.needs_redraw = True
        self.previous_screen = None
        if uses_pygame:
            import pygame
            self.window = pygame.display.set_mode((640, 480))

    def _render_text_mode(self, text_elements):
        if self.needs_redraw:
            [print(text_element) for text_element in text_elements]
            self.needs_redraw = False  # Text only needs to be drawn once

    def _render_graphical_mode(self, ui_elements):
        import pygame
        self.window.fill((255, 255, 255))  # clear the window
        # No animations yet
        # [ui_element.render(self.client_state.clock.get(), self.window) for ui_element in ui_elements]
        [ui_element.render(self.window) for ui_element in ui_elements]
        pygame.display.update()

    def render(self, screen):
        if screen != self.previous_screen:
            self.needs_redraw = True
            self.previous_screen = screen
        self._render_text_mode(screen.get_text_elements())

        if self.uses_pygame:
            self._render_graphical_mode(screen.get_ui_elements())
