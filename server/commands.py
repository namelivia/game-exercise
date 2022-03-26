from abc import ABC, abstractmethod
from .game import Game
from .errors import InvalidCommandError
import pickle
import logging

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
            return pickle.load(open("server_data/games/" + str(game_id), "rb"))
        except FileNotFoundError:
            logger.info("Invalid game id")
            raise InvalidCommandError("Invalid game id")

    # Create a new game
    def create_game(self, name, player_id):
        return Game(name, player_id)

    def save_game(self, new_game: Game):
        pickle.dump(new_game, open("server_data/games/" + str(new_game.id), "wb"))


class PlaceSymbol(Command):
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position

    @property
    def name(self):
        return "Place a symbol on the board"

    def debug(self):
        logger.info(f"Game {self.game_id}: Player {self.player_id} placed a symbol on {self.position}")

    def execute(self):
        super().execute()
        game = self.load_game(self.game_id)
        game.place(self.player_id, self.position)
        self.save_game(game)
        return game


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
        return game


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
        return game
