from unittest import TestCase
from server.engine.commands import CreateGame, JoinGame, GameStatus, GetGameList
from server.game.game import Game
from common.messages import (
    GameMessage,
    GameListResponseMessage,
)
from common.events import GameCreated, PlayerJoined
import mock


class TestServer(TestCase):
    def setUp(self):
        pass

    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("uuid.uuid4")
    def test_creating_a_game(self, m_uuid, m_save_game):
        m_uuid.return_value = "game_id"
        response = CreateGame("test_name", "test_player_id").execute()
        assert isinstance(response, GameMessage)
        assert response.id == "game_id"
        assert response.name == "test_name"
        assert response.players == ["test_player_id"]
        assert len(response.events) == 1
        assert isinstance(response.events[0], GameCreated)
        assert response.events[0].player_id == "test_player_id"
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("server.engine.persistence.Persistence.save_game")
    @mock.patch("uuid.uuid4")
    def test_joining_a_game(self, m_uuid, m_save_game, m_load_game):
        m_uuid.return_value = "game_id"
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = JoinGame("game_id", "player_2_id").execute()
        m_load_game.assert_called_once_with("game_id")
        assert isinstance(response, GameMessage)
        assert response.id == "game_id"
        assert response.name == "test_name"
        assert response.players == ["player_1_id", "player_2_id"]
        assert len(response.events) == 2
        assert isinstance(response.events[0], GameCreated)
        assert response.events[0].player_id == "player_1_id"
        assert isinstance(response.events[1], PlayerJoined)
        assert response.events[1].player_id == "player_2_id"
        m_save_game.assert_called_once()  # TODO: Assert the parameters passed here

    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("uuid.uuid4")
    def test_getting_game_status(self, m_uuid, m_load_game):
        m_uuid.return_value = "game_id"
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = GameStatus("game_id", "player_1_id").execute()
        m_load_game.assert_called_once_with("game_id")
        assert isinstance(response, GameMessage)
        assert response.id == "game_id"
        assert response.name == "test_name"
        assert response.players == ["player_1_id"]
        assert len(response.events) == 1
        assert isinstance(response.events[0], GameCreated)
        assert response.events[0].player_id == "player_1_id"

    @mock.patch("server.engine.persistence.Persistence.get_all_games")
    @mock.patch("server.engine.persistence.Persistence.load_game")
    @mock.patch("uuid.uuid4")
    def test_getting_game_list(self, m_uuid, m_load_game, m_get_all_games):
        m_uuid.return_value = "game_id"
        m_get_all_games.return_value = ["game_1_id", "game_2_id"]
        m_load_game.return_value = Game("test_name", "player_1_id")
        response = GetGameList().execute()
        assert isinstance(response, GameListResponseMessage)
        assert len(response.games) == 2
        assert response.games[0].id == "game_id"
        assert response.games[1].name == "test_name"
        assert response.games[1].id == "game_id"
        assert response.games[0].name == "test_name"
        m_load_game.assert_called()  # TODO: This assertion could be better
