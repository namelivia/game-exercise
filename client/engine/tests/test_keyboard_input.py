from unittest import TestCase

import mock

from client.engine.foundational_wrapper import FoundationalWrapper
from client.engine.input.keyboard import KeyboardInput


class TestInput(TestCase):
    def setUp(self):
        self.keyboard_input = KeyboardInput(True)

    def test_main_loop_iteration(self):
        events = [
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_a, unicode="a"),
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_e, unicode="e"),
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_RETURN, unicode=None),
            mock.Mock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=None),pygamepygame
            mock.Mock(type="UNMAPED_EVENT", key="unknown"),
        ]
        result = self.keyboard_input.read(events)
        assert result == ["a", "e", "return", "backspace"]
