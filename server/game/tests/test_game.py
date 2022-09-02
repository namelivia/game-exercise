from unittest import TestCase
from server.game.game import Game
from common.events import (
    PlayerJoined,
    GameCreated,
    ChatMessageEvent,
    PlayerWins,
)
from server.engine.errors import InvalidCommandError


class TestGame(TestCase):
    def setUp(self):
        pass

    def test_game_initialization(self):
        game = Game("Test game", "player_1_id")
        assert game.players == ["player_1_id"]
        assert len(game.events) == 1
        last_event = game.events[0]
        assert game.winner is None
        assert isinstance(last_event, GameCreated)

    def test_player_joins_game(self):
        player_id = "player_2_id"
        game = Game("Test game", "player_1_id")
        game.join(player_id)
        assert game.players == ["player_1_id", "player_2_id"]
        assert len(game.events) == 2
        last_event = game.events[1]
        assert isinstance(last_event, PlayerJoined)
        assert last_event.player_id == "player_2_id"

    def test_player_cannot_join_game_if_full(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")

        with self.assertRaises(InvalidCommandError) as e:
            game.join("player_3_id")
        assert len(game.players) == 2
        assert isinstance(e.exception, InvalidCommandError)
        assert str(e.exception) == "The game is full"

    def test_player_cannot_join_twice(self):
        game = Game("Test game", "player_1_id")
        game.join("player_1_id")
        assert game.players == ["player_1_id"]
        assert len(game.events) == 1

    def test_only_players_in_games_can_get_status(self):
        game = Game("Test game", "player_1_id")
        game.player_can_get_status("player_1_id")
        with self.assertRaises(InvalidCommandError) as e:
            game.player_can_get_status("other_player_id")
        assert str(e.exception) == "Player has no access to the game"

    def test_sending_a_chat_message(self):
        game = Game("Test game", "player_1_id")
        game.add_chat_message("player_1_id", "hello")
        assert len(game.events) == 2
        last_event = game.events[1]
        assert isinstance(last_event, ChatMessageEvent)
        assert last_event.player_id == "player_1_id"
        assert last_event.message == "hello"

        with self.assertRaises(InvalidCommandError) as e:
            game.add_chat_message("other_player_id", "bye")
        assert str(e.exception) == "Player has no access to the game"
        assert len(game.events) == 2

    def test_only_players_in_games_can_get_place_symbols(self):
        game = Game("Test game", "player_1_id")
        with self.assertRaises(InvalidCommandError) as e:
            game.place("other_player_id", 2)
        assert str(e.exception) == "Player has no access to the game"
        assert len(game.events) == 1

    def test_symbols_cannot_be_placed_until_the_game_is_full(self):
        game = Game("Test game", "player_1_id")
        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_1_id", 2)
        assert str(e.exception) == "No player 2 yet"
        assert len(game.events) == 1

    def test_symbols_can_only_be_placed_when_is_player_turn(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")
        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_2_id", 0)
        assert str(e.exception) == "Not your turn"
        assert len(game.events) == 2

        game.place("player_1_id", 0)  # Player 1 places, now it is player's 2 turn
        assert len(game.events) == 3

        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_1_id", 2)
        assert str(e.exception) == "Not your turn"
        assert len(game.events) == 3

        game.place("player_2_id", 1)  # Player 2 places
        assert len(game.events) == 4

    def test_symbols_cannot_be_taken_twice_in_the_same_place(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")

        game.place("player_1_id", 0)
        assert len(game.events) == 3

        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_2_id", 0)  # Same position as Player 1
        assert str(e.exception) == "Position already taken"
        assert len(game.events) == 3

    def test_player_cant_place_out_of_bounds(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")

        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_1_id", 99)
        assert str(e.exception) == "Position out of bounds"
        assert len(game.events) == 2

    def test_player_cant_place_if_game_is_finished(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")
        game.winner = "player_1_id"  # A winner is set, the game is finished

        with self.assertRaises(InvalidCommandError) as e:
            game.place("player_1_id", 0)
        assert str(e.exception) == "The game is already finished"
        assert len(game.events) == 2

    def test_when_user_makes_a_line_wins_the_game(self):
        game = Game("Test game", "player_1_id")
        game.join("player_2_id")

        # _ _  _
        # _ _  _
        # _ _  _

        game.place("player_1_id", 0)

        # 1 _  _
        # _ _  _
        # _ _  _

        game.place("player_2_id", 2)

        # 1 _  2
        # _ _  _
        # _ _  _

        game.place("player_1_id", 3)

        # 1 _  2
        # 1 _  _
        # _ _  _

        game.place("player_2_id", 5)

        # 1 _  2
        # 1 _  2
        # _ _  _

        assert game.winner is None
        game.place("player_1_id", 6)

        # 1 _  2
        # 1 _  2
        # 1 _  _

        assert len(game.events) == 8
        assert game.board == [
            "player_1_id",
            None,
            "player_2_id",
            "player_1_id",
            None,
            "player_2_id",
            "player_1_id",
            None,
            None,
        ]
        assert game.winner == "player_1_id"
        last_event = game.events[7]
        assert isinstance(last_event, PlayerWins)
        assert last_event.player_id == "player_1_id"

    def test_different_winning_combinations(self):
        game = Game("Test game", "player_1_id")

        game.board = [
            "player_1_id",
            None,
            "player_2_id",
            "player_1_id",
            None,
            "player_2_id",
            None,
            None,
            None,
        ]
        assert game._check_if_there_is_a_winner() is None

        game.board = [
            "player_1_id",
            None,
            "player_2_id",
            "player_1_id",
            None,
            "player_2_id",
            None,
            "player_1_id",
            "player_2_id",
        ]
        assert game._check_if_there_is_a_winner() == "player_2_id"

        game.board = [
            "player_1_id",
            "player_2_id",
            None,
            "player_2_id",
            "player_1_id",
            "player_2_id",
            "player_2_id",
            None,
            "player_1_id",
        ]
        assert game._check_if_there_is_a_winner() == "player_1_id"
