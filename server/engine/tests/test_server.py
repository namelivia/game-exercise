from unittest import TestCase
from server.engine.commands import CreateGame, JoinGame, GameStatus, GetGameList
from server.game.game import Game
from common.messages import (
    GameInfoMessage,
    GameEventsMessage,
    GameListResponseMessage,
)
from common.events import ChatMessageEvent
import mock

UUID = "760be8c0-13bd-428e-86e3-10632d1bbd6e"


class TestServer(TestCase):
    def setUp(self):
        pass

    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("server.game.game.uuid4")
    def test_creating_a_game(self, m_uuid, m_save_game):
        m_uuid.return_value = UUID
        response = CreateGame("test_name", "test_player_id").execute()
        assert isinstance(response, GameInfoMessage)
        assert response.id == UUID
        assert response.name == "test_name"
        assert response.players == ["test_player_id"]
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("server.game.game.uuid4")
    def test_joining_a_game(self, m_uuid, m_save_game, m_load_game):
        m_uuid.return_value = UUID
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = JoinGame(UUID, "player_2_id").execute()
        m_load_game.assert_called_once_with(UUID)
        assert isinstance(response, GameInfoMessage)
        assert response.id == UUID
        assert response.name == "test_name"
        assert response.players == ["player_1_id", "player_2_id"]
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("server.game.game.uuid4")
    def test_getting_game_status(self, m_uuid, m_load_game):
        # A client is requesting the new events that happened in the game
        # the client has its event pointer set at 2 so only events 3 and 4 are sent.
        m_uuid.return_value = UUID
        mocked_game = Game("test_name", "player_1_id")
        mocked_game.events += [
            ChatMessageEvent("id_1", "player_1_id", "message1"),
            ChatMessageEvent("id_2", "player_1_id", "message2"),
            ChatMessageEvent("id_3", "player_1_id", "message3"),
        ]
        m_load_game.return_value = mocked_game
        # When requesting the pointer is set to 2
        response = GameStatus(UUID, 2, "player_1_id").execute()
        m_load_game.assert_called_once_with(UUID)
        assert isinstance(response, GameEventsMessage)
        assert len(response.events) == 2
        assert isinstance(response.events[0], ChatMessageEvent)
        assert response.events[0].event_id == "id_2"
        assert response.events[0].message == "message2"
        assert isinstance(response.events[1], ChatMessageEvent)
        assert response.events[1].event_id == "id_3"
        assert response.events[1].message == "message3"

    @mock.patch("server.engine.persistence.Persistence.get_all_games")
    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("server.game.game.uuid4")
    def test_getting_game_list(self, m_uuid, m_load_game, m_get_all_games):
        m_uuid.return_value = UUID
        m_get_all_games.return_value = [UUID, UUID]
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = GetGameList().execute()
        assert isinstance(response, GameListResponseMessage)
        assert len(response.games) == 2
        assert response.games[0].id == UUID
        assert response.games[1].name == "test_name"
        assert response.games[1].id == UUID
        assert response.games[0].name == "test_name"
        m_load_game.assert_called()  # TODO: This assertion could be better
