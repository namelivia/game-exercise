from unittest import TestCase
from server.engine.commands import SendChat, PlaceSymbol
from common.messages import ChatMessageConfirmation, SymbolPlacedConfirmation
from mock import patch, Mock


class TestCommands(TestCase):
    def setUp(self):
        pass

    @patch("server.engine.commands.Persistence.save_game")
    @patch("server.engine.commands.Persistence.load_game")
    def test_chat_command(self, m_load, m_save):
        m_game = Mock()
        m_load.return_value = m_game

        # A send chat event is invoked
        response = SendChat(
            "game_id", "event_id", "player_id", "some message"
        ).execute()

        # The chat message event is added to the game
        m_load.assert_called_once_with("game_id")
        m_game.add_chat_message.assert_called_once_with(
            "event_id", "player_id", "some message"
        )
        m_save.assert_called_once_with(m_game)

        # A message confirmation is returned to the creator of the chat message
        assert isinstance(response, ChatMessageConfirmation)
        assert response.event_id == "event_id"

    @patch("server.engine.commands.Persistence.save_game")
    @patch("server.engine.commands.Persistence.load_game")
    def test_place_symbol_command(self, m_load, m_save):
        m_game = Mock()
        m_load.return_value = m_game

        # A place symbol event is invoked
        response = PlaceSymbol("game_id", "event_id", "player_id", 3).execute()

        # The place symbol event is added to the game
        m_load.assert_called_once_with("game_id")
        m_game.place.assert_called_once_with("event_id", "player_id", 3)
        m_save.assert_called_once_with(m_game)

        # A confirmation is returned to the creator of the place symbol event
        assert isinstance(response, SymbolPlacedConfirmation)
        assert response.event_id == "event_id"
