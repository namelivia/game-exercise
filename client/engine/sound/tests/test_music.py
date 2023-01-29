from unittest import TestCase
from mock import patch
from .music import Music


class TestMusic(TestCase):
    @patch("pygame.mixer.music.load")
    def test_playing_a_song(self, m_pygame_load_song):
        path = "some/sound/file.mp3"
        Music.load(path)
        m_pygame_load_song.assert_called_once_with(path)

    @patch("pygame.mixer.music.play")
    def test_play_loaded_song(self, m_pygame_play_song):
        Music.play()
        m_pygame_play_song.assert_called_once_with(-1)

    @patch("pygame.mixer.music.stop")
    def test_stop_loaded_song(self, m_pygame_stop_song):
        Music.stop()
        m_pygame_stop_song.assert_called_once_with()
