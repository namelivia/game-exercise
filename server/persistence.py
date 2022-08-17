import pickle
from os import walk
from .game import Game

GAMES_PATH = "server_data/games/"


class Persistence:
    @staticmethod
    def load_game(game_id: str):
        return pickle.load(open(f"{GAMES_PATH}{game_id}", "rb"))

    @staticmethod
    def save_game(new_game: Game):
        pickle.dump(new_game, open(GAMES_PATH + str(new_game.id), "wb"))

    @staticmethod
    def get_all_games():
        return next(walk(GAMES_PATH))[2]
