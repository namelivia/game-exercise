class Profile():
    def __init__(self, id, name, game_id):
        self.id = id
        self.name = name
        self.game_id = game_id

    def set_game(self, game_id):
        self.game_id = game_id
