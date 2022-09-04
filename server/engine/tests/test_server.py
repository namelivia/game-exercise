from unittest import TestCase
from server.engine.commands import CreateGame, JoinGame, GameEventsPage, GetGameList
from server.game.game import Game
from common.messages import (
    GameInfoMessage,
    GameEventsPageMessage,
    GameListResponsePageMessage,
)
from common.events import GameCreated
import mock


class TestServer(TestCase):
    def setUp(self):
        pass

    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("uuid.uuid4")
    def test_creating_a_game(self, m_uuid, m_save_game):
        m_uuid.return_value = "game_id"
        response = CreateGame("test_name", "test_player_id").execute()
        assert isinstance(response, GameInfoMessage)
        assert response.id == "game_id"
        assert response.name == "test_name"
        assert response.players == ["test_player_id"]
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("uuid.uuid4")
    def test_joining_a_game(self, m_uuid, m_save_game, m_load_game):
        m_uuid.return_value = "game_id"
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = JoinGame("game_id", "player_2_id").execute()
        m_load_game.assert_called_once_with("game_id")
        assert isinstance(response, GameInfoMessage)
        assert response.id == "game_id"
        assert response.name == "test_name"
        assert response.players == ["player_1_id", "player_2_id"]
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("uuid.uuid4")
    def test_getting_game_events_page(self, m_uuid, m_load_game):
        # TODO: This is just a game with 1 event, for testing pagination
        # property create a game with many events
        m_uuid.return_value = "game_id"
        m_load_game.return_value = Game("test_name", "player_1_id")
        # Askin for page 0
        response = GameEventsPage("game_id", 0, "player_1_id").execute()
        m_load_game.assert_called_once_with("game_id")
        assert isinstance(response, GameEventsPageMessage)
        assert len(response.events) == 1
        assert isinstance(response.events[0], GameCreated)
        assert response.events[0].player_id == "player_1_id"
        assert response.next_page is None
        assert response.page == 0

    @mock.patch("server.engine.persistence.Persistence.get_all_games")
    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("uuid.uuid4")
    def test_getting_game_list(self, m_uuid, m_load_game, m_get_all_games):
        m_uuid.return_value = "game_id"
        m_get_all_games.return_value = ["game_1_id", "game_2_id"]
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = GetGameList().execute()
        assert isinstance(response, GameListResponsePageMessage)
        assert len(response.games) == 2
        assert response.games[0].id == "game_id"
        assert response.games[1].name == "test_name"
        assert response.games[1].id == "game_id"
        assert response.games[0].name == "test_name"
        m_load_game.assert_called()  # TODO: This assertion could be better
