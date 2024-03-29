from unittest import TestCase

from mock import Mock, patch

from client.engine.sound.sound import Sound


class TestSound(TestCase):
    @patch("pygame.mixer.Sound")
    def test_playing_a_sound(self, m_pygame_sound):
        pygame_sound_file = Mock()
        m_pygame_sound.play = Mock()
        m_pygame_sound.return_value = pygame_sound_file
        path = "some/sound/file.mp3"
        Sound.play(path)
        m_pygame_sound.assert_called_once_with(path)
        m_pygame_sound.play.assert_called_once_with(pygame_sound_file)
