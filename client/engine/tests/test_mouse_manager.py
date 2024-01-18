from unittest import TestCase

import mock
import pygame

from client.engine.input.mouse_manager import MouseManager


class TestInputManager(TestCase):
    def setUp(self):
        self.mouse_manager = MouseManager()

    @mock.patch("pygame.event.get")
    def test_main_loop_iteration(self, m_pygame_get):
        m_pygame_get.return_value = [
            mock.Mock(type=pygame.MOUSEBUTTONDOWN),
        ]
        result = self.mouse_manager.read()
        m_pygame_get.assert_called_once_with()
        assert result == []
