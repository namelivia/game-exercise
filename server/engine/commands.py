from abc import ABC, abstractmethod
from server.game.game import Game
from .errors import InvalidCommandError
from .persistence import Persistence
import logging
from common.messages import (
    GameMessage,
    PingResponseMessage,
    GameListResponseMessage,
    GameListResponseEntry,
)

logger = logging.getLogger(__name__)

"""
These are the commands that can be received from the server.
All the commands do the following:
1 - Load game
2 - Execute game operation
3 - Save the game
4 - And return it
"""


class Command(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def debug(self):
        pass

    def execute(self):
        self.debug()

    # Retrieve the current game from storage
    def load_game(self, game_id):
        try:
            return Persistence.load_game(str(game_id))
        except FileNotFoundError:
            logger.info("Invalid game id")
            raise InvalidCommandError("Invalid game id")

    # Create a new game
    def create_game(self, name, player_id):
        return Game(name, player_id)

    def save_game(self, new_game: Game):
        Persistence.save_game(new_game)


class PlaceSymbol(Command):
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position

    @property
    def name(self):
        return "Place a symbol on the board"

    def debug(self):
        logger.info(
            f"Game {self.game_id}: Player {self.player_id} placed a symbol on {self.position}"
        )

    def execute(self):
        super().execute()
        game = self.load_game(self.game_id)
        game.place(self.player_id, self.position)
        self.save_game(game)
        return GameMessage(game)


class SendChat(Command):
    def __init__(self, game_id, player_id, message):
        self.game_id = game_id
        self.player_id = player_id
        self.message = message

    @property
    def name(self):
        return "Send chat message"

    def debug(self):
        logger.info(
            f"Game {self.game_id}: Player {self.player_id} says: {self.message}"
        )

    def execute(self):
        super().execute()
        game = self.load_game(self.game_id)
        game.add_chat_message(self.player_id, self.message)
        self.save_game(game)
        return GameMessage(game)


class CreateGame(Command):
    def __init__(self, game_name, player_id):
        self.game_name = game_name
        self.player_id = player_id

    @property
    def name(self):
        return "Create a new game"

    def debug(self):
        logger.info(f"Player {self.player_id} created a game called {self.game_name}")

    def execute(self):
        super().execute()
        game = self.create_game(self.game_name, self.player_id)
        # Persist the new game on storage
        self.save_game(game)
        return GameMessage(game)


class JoinGame(Command):
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id

    def name(self):
        return "Join an existing game"

    def debug(self):
        logger.info(f"Game {self.game_id}: Player {self.player_id} is joining")

    def execute(self):
        super().execute()
        game = self.load_game(self.game_id)
        game.join(self.player_id)
        self.save_game(game)
        return GameMessage(game)


class GameStatus(Command):
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id

    def name(self):
        return "Get game status"

    def debug(self):
        logger.info(f"Player {self.player_id} requested info for game: {self.game_id}")

    def execute(self):
        super().execute()
        game = self.load_game(self.game_id)
        game.player_can_get_status(self.player_id)
        return GameMessage(game)


class Ping(Command):
    def name(self):
        return "Ping"

    def debug(self):
        logger.info("Ping request")

    def execute(self):
        super().execute()
        return PingResponseMessage()


class GetGameList(Command):
    @property
    def name(self):
        return "Get game list"

    def debug(self):
        logger.info("Game list request")

    def _build_index_entry_from_game(self, game_id):
        game = Persistence.load_game(game_id)
        return GameListResponseEntry(game)

    def _build_index_from_games(self, game_ids):
        return [self._build_index_entry_from_game(game_id) for game_id in game_ids]

    # Retrieve the list of games current game from storage
    def get_all_games(self):
        return Persistence.get_all_games()

    def execute(self):
        super().execute()
        game_ids = self.get_all_games()
        return GameListResponseMessage(self._build_index_from_games(game_ids))