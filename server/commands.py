from abc import ABC
from .game import Game
from .errors import InvalidCommandError
import pickle


class Command(ABC):
    # Retrieve the current game from storage
    def load_game(self, game_id):
        try:
            return pickle.load(open("games/" + str(game_id), "rb"))
        except FileNotFoundError:
            raise InvalidCommandError("Invalid game id")

    # Create a new game
    def create_game(self, name, player_id):
        return Game(name, player_id)

    def save_game(self, new_game: Game):
        pickle.dump(new_game, open("games/" + str(new_game.id), "wb"))

    def execute(self):
        pass


class PlaceSymbol(Command):
    def __init__(self, game_id, player_id, position):
        self.game_id = game_id
        self.player_id = player_id
        self.position = position

    def execute(self):
        game = self.load_game(self.game_id)
        game.place(self.player_id, self.position)
        self.save_game(game)
        return game


class CreateGame(Command):
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def execute(self):
        game = self.create_game(self.name, self.player_id)
        # Persist the new game on storage
        self.save_game(game)
        return game


class JoinGame(Command):
    def __init__(self, game_id, player_id):
        self.game_id = game_id
        self.player_id = player_id

    def execute(self):
        game = self.load_game(self.game_id)
        game.join(self.player_id)
        self.save_game(game)
        return game
