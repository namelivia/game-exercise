from unittest import TestCase

import mock
import pygame

from client.engine.input.keyboard_manager import KeyboardManager


class TestInputManager(TestCase):
    def setUp(self):
        self.keyboard_manager = KeyboardManager()

    @mock.patch("pygame.event.get")
    def test_main_loop_iteration(self, m_pygame_get):
        m_pygame_get.return_value = [
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_a),
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_e),
            mock.Mock(type="UNMAPED_EVENT", key="unknown"),
        ]
        result = self.keyboard_manager.read()
        m_pygame_get.assert_called_once_with()
        assert result == ["event_a", "event_e"]
