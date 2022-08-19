from unittest import TestCase
from client.game.screens.new_game.new_game import NewGame
from client.events import UserTypedEvent
import numpy
import mock


class TestNewGame(TestCase):
    def setUp(self):
        self.client_state = mock.Mock()
        self.client_state.clock.get.return_value = 0  # Initial time is 0
        self.new_game = NewGame(self.client_state)

    def _render_surface(self, screen):
        '''
        Renders a new surface to be compared
        '''
        ui_elements = screen.get_ui_elements()
        import pygame

        pygame.init()
        surface = pygame.Surface((640, 480))
        surface.fill((255, 255, 255))  # Clear the surface
        [ui_element.render(surface) for ui_element in ui_elements]
        return surface

    def _matches_snapshot(self, screen, snapshot_key):
        import pygame
        new_surface = self._render_surface(screen)
        # Convert matches the image pixel depth to the original surface
        screenshot = pygame.image.load(snapshot_key).convert(new_surface)
        new_array = pygame.surfarray.array2d(new_surface)
        screenshot_array = pygame.surfarray.array2d(screenshot)

        numpy.testing.assert_array_equal(new_array, screenshot_array)

    @mock.patch("client.commands.RequestGameCreation")
    def test_new_game_screen(self, m_request_game_creation):

        # User types the word test
        self.new_game.update(
            UserTypedEvent("t"),
        )
        self.new_game.update(
            UserTypedEvent("e"),
        )
        self.new_game.update(
            UserTypedEvent("s"),
        )
        self.new_game.update(
            UserTypedEvent("t"),
        )

        # Typo
        self.new_game.update(
            UserTypedEvent("z"),
        )
        # Deleting last letter
        self.new_game.update(
            UserTypedEvent("backspace"),
        )

        self._matches_snapshot(
            self.new_game,
            "./client/game/screens/new_game/tests/screenshots/new_game_test_input.png")

        # User presses enter and creates the new game
        self.new_game.update(
            UserTypedEvent("return"),
        )
        m_request_game_creation.assert_called_once_with(mock.ANY, mock.ANY, "test")
